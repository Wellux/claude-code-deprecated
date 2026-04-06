import jwt from 'jsonwebtoken';
import { config } from '../config';

/**
 * Service zur Handhabung von JWT Tokens
 * Verantwortlich für Token-Generierung und -Validierung
 */
export class JwtService {
  /**
   * Generiert ein JWT-Token für einen authentifizierten Benutzer
   * @param payload Die Daten, die im Token gespeichert werden sollen
   * @returns Das generierte JWT-Token
   */
  public generateToken(payload: { userId: string; email: string }): string {
    return jwt.sign(payload, config.jwt.secret, {
      expiresIn: config.jwt.expiresIn,
    });
  }

  /**
   * Validiert ein JWT-Token und gibt die enthaltenen Daten zurück
   * @param token Das zu validierende Token
   * @returns Die im Token enthaltenen Daten
   * @throws Error, wenn das Token ungültig oder abgelaufen ist
   */
  public verifyToken(token: string): { userId: string; email: string } {
    try {
      const decoded = jwt.verify(token, config.jwt.secret) as { userId: string; email: string };
      return decoded;
    } catch (error) {
      throw new Error('Ungültiges oder abgelaufenes Token');
    }
  }
}
