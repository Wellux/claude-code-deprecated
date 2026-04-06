import { Request, Response } from 'express';
import { AuthService } from '../services/auth.service';
import { UserLoginDto, UserRegistrationDto } from '../types/user.types';

/**
 * Controller für die Authentifizierungs-Endpunkte
 */
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  /**
   * Registriert einen neuen Benutzer
   * @param req Express Request-Objekt
   * @param res Express Response-Objekt
   */
  public async register(req: Request, res: Response): Promise<void> {
    try {
      const userData = req.body as UserRegistrationDto;
      const user = await this.authService.registerUser(userData);
      
      res.status(201).json({
        success: true,
        message: 'Benutzer erfolgreich registriert',
        data: user,
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error instanceof Error ? error.message : 'Ein Fehler ist aufgetreten',
      });
    }
  }

  /**
   * Authentifiziert einen Benutzer
   * @param req Express Request-Objekt
   * @param res Express Response-Objekt
   */
  public async login(req: Request, res: Response): Promise<void> {
    try {
      const loginData = req.body as UserLoginDto;
      const { token, user } = await this.authService.loginUser(loginData);
      
      // Token als HTTP-Only-Cookie setzen für verbesserte Sicherheit
      res.cookie('auth_token', token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        maxAge: 24 * 60 * 60 * 1000, // 1 Tag
        sameSite: 'strict',
      });
      
      res.status(200).json({
        success: true,
        message: 'Erfolgreich angemeldet',
        data: {
          user,
          token, // Token auch in der Antwort senden für Client-seitige Speicherung (falls gewünscht)
        },
      });
    } catch (error) {
      res.status(401).json({
        success: false,
        message: error instanceof Error ? error.message : 'Anmeldung fehlgeschlagen',
      });
    }
  }

  /**
   * Meldet einen Benutzer ab
   * @param req Express Request-Objekt
   * @param res Express Response-Objekt
   */
  public async logout(_req: Request, res: Response): Promise<void> {
    // Cookie löschen
    res.clearCookie('auth_token');
    
    res.status(200).json({
      success: true,
      message: 'Erfolgreich abgemeldet',
    });
  }
}
