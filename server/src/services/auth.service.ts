import bcrypt from 'bcrypt';
import { UserRepository } from '../repositories/user.repository';
import { JwtService } from './jwt.service';
import { 
  LoginResponse, 
  SafeUserInfo, 
  UserLoginDto, 
  UserRegistrationDto 
} from '../types/user.types';

/**
 * Auth Service
 * 
 * Implementiert die Geschäftslogik für Authentifizierung und Autorisierung
 */
export class AuthService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly jwtService: JwtService
  ) {}

  /**
   * Registriert einen neuen Benutzer
   * @param userData Die Registrierungsdaten des Benutzers
   * @returns Die sicheren Benutzerinformationen ohne Passwort
   * @throws Error, wenn bereits ein Benutzer mit dieser E-Mail existiert
   */
  public async registerUser(userData: UserRegistrationDto): Promise<SafeUserInfo> {
    // Prüfen, ob bereits ein Benutzer mit dieser E-Mail existiert
    const existingUser = await this.userRepository.findByEmail(userData.email);
    
    if (existingUser) {
      throw new Error('Ein Benutzer mit dieser E-Mail-Adresse existiert bereits');
    }
    
    // Passwort hashen
    const hashedPassword = await bcrypt.hash(userData.password, 10);
    
    // Benutzer erstellen
    const newUser = await this.userRepository.createUser({
      ...userData,
      password: hashedPassword,
    });
    
    // Sichere Benutzerinformationen zurückgeben (ohne Passwort)
    return this.toSafeUserInfo(newUser);
  }

  /**
   * Authentifiziert einen Benutzer
   * @param loginData Die Login-Daten des Benutzers
   * @returns Ein JWT-Token und die Benutzerinformationen bei erfolgreicher Authentifizierung
   * @throws Error, wenn die Authentifizierung fehlschlägt
   */
  public async loginUser(loginData: UserLoginDto): Promise<LoginResponse> {
    // Benutzer anhand der E-Mail suchen
    const user = await this.userRepository.findByEmail(loginData.email);
    
    if (!user) {
      throw new Error('Ungültige E-Mail-Adresse oder Passwort');
    }
    
    // Passwort überprüfen
    const isPasswordValid = await bcrypt.compare(loginData.password, user.password);
    
    if (!isPasswordValid) {
      throw new Error('Ungültige E-Mail-Adresse oder Passwort');
    }
    
    // JWT-Token generieren
    const token = this.jwtService.generateToken({
      userId: user.id,
      email: user.email,
    });
    
    // Token und sichere Benutzerinformationen zurückgeben
    return {
      token,
      user: this.toSafeUserInfo(user),
    };
  }

  /**
   * Konvertiert ein User-Objekt in ein SafeUserInfo-Objekt (ohne Passwort)
   * @param user Das User-Objekt
   * @returns Ein SafeUserInfo-Objekt
   */
  private toSafeUserInfo(user: { id: string; name: string; email: string }): SafeUserInfo {
    return {
      id: user.id,
      name: user.name,
      email: user.email,
    };
  }
}
