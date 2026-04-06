import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import morgan from 'morgan';
import cookieParser from 'cookie-parser';
import rateLimit from 'express-rate-limit';
import { Router } from 'express';
import { config } from './config';

// Services
import { JwtService } from './services/jwt.service';
import { AuthService } from './services/auth.service';

// Repositories
import { UserRepository } from './repositories/user.repository';

// Controller
import { AuthController } from './controllers/auth.controller';

// Middleware
import { AuthMiddleware } from './middleware/auth.middleware';

// Routes
import { configureAuthRoutes } from './routes/auth.routes';

/**
 * Server-Klasse
 * 
 * Verantwortlich für die Konfiguration und den Start des Express-Servers
 */
class Server {
  private app = express();
  private readonly port: number = config.server.port;
  private readonly apiRouter = Router();
  
  // Repositories
  private readonly userRepository = new UserRepository();
  
  // Services
  private readonly jwtService = new JwtService();
  private readonly authService = new AuthService(this.userRepository, this.jwtService);
  
  // Middleware
  private readonly authMiddleware = new AuthMiddleware(this.jwtService, this.userRepository);
  
  // Controller
  private readonly authController = new AuthController(this.authService);

  constructor() {
    this.configureMiddleware();
    this.configureRoutes();
    this.configureErrorHandling();
  }

  /**
   * Konfiguriert die globale Middleware
   */
  private configureMiddleware(): void {
    // Sicherheitseinstellungen
    this.app.use(helmet());
    this.app.use(
      cors({
        origin: config.cors.origin,
        credentials: true,
      })
    );
    
    // Rate-Limiting zum Schutz vor Brute-Force-Angriffen
    this.app.use(
      rateLimit({
        windowMs: 15 * 60 * 1000, // 15 Minuten
        max: 100, // Max 100 Anfragen pro IP innerhalb des Zeitfensters
        standardHeaders: true,
        legacyHeaders: false,
      })
    );
    
    // Request-Parsing
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));
    this.app.use(cookieParser());
    
    // Logging
    this.app.use(morgan(config.env === 'production' ? 'combined' : 'dev'));
  }

  /**
   * Konfiguriert die API-Routen
   */
  private configureRoutes(): void {
    // Auth-Routen
    configureAuthRoutes(this.apiRouter, this.authController, this.authMiddleware);
    
    // API-Routen unter /api mounten
    this.app.use('/api', this.apiRouter);
    
    // Root-Route für Healthcheck
    this.app.get('/', (_req, res) => {
      res.status(200).json({
        status: 'ok',
        message: 'WelluxAI API läuft',
        version: '1.0.0',
      });
    });
  }

  /**
   * Konfiguriert die Fehlerbehandlung
   */
  private configureErrorHandling(): void {
    // 404-Handler für nicht gefundene Routen
    this.app.use((_req, res) => {
      res.status(404).json({
        success: false,
        message: 'Route nicht gefunden',
      });
    });
    
    // Globaler Fehlerhandler
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    this.app.use((err: any, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
      const statusCode = err.statusCode || 500;
      const message = err.message || 'Interner Serverfehler';
      
      console.error(`[ERROR] ${message}`, err);
      
      res.status(statusCode).json({
        success: false,
        message,
        ...(config.env !== 'production' && { stack: err.stack }),
      });
    });
  }

  /**
   * Startet den Server
   */
  public start(): void {
    this.app.listen(this.port, () => {
      console.log(`Server läuft auf Port ${this.port} in ${config.env}-Modus`);
    });
  }
}

// Server-Instanz erstellen und starten
const server = new Server();
server.start();
