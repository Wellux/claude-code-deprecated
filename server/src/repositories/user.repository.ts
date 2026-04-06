import { User, UserRegistrationDto } from '../types/user.types';

/**
 * User Repository
 * 
 * In einer produktiven Anwendung würde dieses Repository eine Datenbank verwenden.
 * Für diese Implementierung verwenden wir eine In-Memory-Datenbank als Simulation.
 * In einer echten Anwendung würde hier MongoDB, PostgreSQL oder ein anderes DBMS angebunden werden.
 */
export class UserRepository {
  private users: Record<string, User> = {};

  /**
   * Findet einen Benutzer anhand seiner E-Mail-Adresse
   * @param email Die zu suchende E-Mail-Adresse
   * @returns Der gefundene Benutzer oder null, wenn kein Benutzer gefunden wurde
   */
  public async findByEmail(email: string): Promise<User | null> {
    const user = Object.values(this.users).find(u => u.email === email);
    return user || null;
  }

  /**
   * Findet einen Benutzer anhand seiner ID
   * @param id Die zu suchende Benutzer-ID
   * @returns Der gefundene Benutzer oder null, wenn kein Benutzer gefunden wurde
   */
  public async findById(id: string): Promise<User | null> {
    return this.users[id] || null;
  }

  /**
   * Erstellt einen neuen Benutzer
   * @param userData Die Daten des zu erstellenden Benutzers
   * @returns Der erstellte Benutzer
   */
  public async createUser(userData: UserRegistrationDto): Promise<User> {
    const id = this.generateId();
    const now = new Date().toISOString();
    
    const newUser: User = {
      id,
      ...userData,
      created: now,
    };
    
    this.users[id] = newUser;
    return newUser;
  }

  /**
   * Aktualisiert einen bestehenden Benutzer
   * @param id Die ID des zu aktualisierenden Benutzers
   * @param userData Die zu aktualisierenden Daten
   * @returns Der aktualisierte Benutzer oder null, wenn kein Benutzer gefunden wurde
   */
  public async updateUser(id: string, userData: Partial<User>): Promise<User | null> {
    const user = await this.findById(id);
    
    if (!user) {
      return null;
    }
    
    const updatedUser = {
      ...user,
      ...userData,
    };
    
    this.users[id] = updatedUser;
    return updatedUser;
  }

  /**
   * Hilfsmethode zur Generierung einer zufälligen ID
   * In einer echten Anwendung würde dies durch die Datenbank oder einen UUID-Generator erfolgen
   * @returns Eine zufällige ID
   */
  private generateId(): string {
    return `user_${Date.now()}_${Math.floor(Math.random() * 1000)}`;
  }
}
