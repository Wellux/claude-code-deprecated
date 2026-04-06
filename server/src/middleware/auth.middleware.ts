import { Request, Response, NextFunction } from 'express';
import { JwtService } from '../services/jwt.service';
import { UserRepository } from '../repositories/user.repository';

// Erweitere den Express-Request-Typ um den authentifizierten Benutzer
declare global {
  namespace Express {
    interface Request {
      user?: {
        userId: string;
        email: string;
      };
    }
  }
}

/**
 * Middleware zur Authentifizierung von Anfragen mittels JWT
 */
export class AuthMiddleware {
  constructor(
    private readonly jwtService: JwtService,
    private readonly userRepository: UserRepository
  ) {}

  /**
   * Überprüft, ob eine Anfrage einen gültigen JWT-Token enthält
   * und setzt den authentifizierten Benutzer in das Request-Objekt
   */
  public authenticate = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      // Token aus Authorization-Header oder Cookie extrahieren
      const token = this.extractToken(req);
      
      if (!token) {
        res.status(401).json({
          success: false,
          message: 'Authentifizierung erforderlich',
        });
        return;
      }
      
      // Token validieren
      const decodedToken = this.jwtService.verifyToken(token);
      
      // Benutzer in Request-Objekt setzen
      req.user = {
        userId: decodedToken.userId,
        email: decodedToken.email,
      };
      
      next();
    } catch (error) {
      res.status(401).json({
        success: false,
        message: 'Ungültiger oder abgelaufener Token',
      });
    }
  };

  /**
   * Extrahiert den JWT-Token aus dem Request
   * @param req Express Request-Objekt
   * @returns Der extrahierte Token oder null, wenn kein Token gefunden wurde
   */
  private extractToken(req: Request): string | null {
    // Zuerst im Authorization-Header suchen
    const authHeader = req.headers.authorization;
    if (authHeader && authHeader.startsWith('Bearer ')) {
      return authHeader.substring(7);
    }
    
    // Dann im Cookie suchen
    if (req.cookies && req.cookies.auth_token) {
      return req.cookies.auth_token;
    }
    
    return null;
  }
}
