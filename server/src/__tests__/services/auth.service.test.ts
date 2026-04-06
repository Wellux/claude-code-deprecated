import { AuthService } from '../../services/auth.service';
import { UserRepository } from '../../repositories/user.repository';
import { JwtService } from '../../services/jwt.service';
import * as bcrypt from 'bcrypt';

// Mock der Repository-Schicht
jest.mock('../../repositories/user.repository');
jest.mock('../../services/jwt.service');
jest.mock('bcrypt');

describe('AuthService', () => {
  let authService: AuthService;
  let userRepository: jest.Mocked<UserRepository>;
  let jwtService: jest.Mocked<JwtService>;

  beforeEach(() => {
    userRepository = new UserRepository() as jest.Mocked<UserRepository>;
    jwtService = new JwtService() as jest.Mocked<JwtService>;
    authService = new AuthService(userRepository, jwtService);
  });

  describe('registerUser', () => {
    it('should hash the password and create a new user', async () => {
      // Arrange
      const userData = {
        name: 'Test User',
        email: 'test@example.com',
        password: 'Password123!',
      };
      const hashedPassword = 'hashedPassword123';
      const createdUser = {
        id: '1',
        name: userData.name,
        email: userData.email,
        password: hashedPassword,
        created: new Date().toISOString(),
      };

      (bcrypt.hash as jest.Mock).mockResolvedValue(hashedPassword);
      userRepository.createUser.mockResolvedValue(createdUser);
      userRepository.findByEmail.mockResolvedValue(null);

      // Act
      const result = await authService.registerUser(userData);

      // Assert
      expect(userRepository.findByEmail).toHaveBeenCalledWith(userData.email);
      expect(bcrypt.hash).toHaveBeenCalledWith(userData.password, 10);
      expect(userRepository.createUser).toHaveBeenCalledWith({
        ...userData,
        password: hashedPassword,
      });
      expect(result).toEqual({
        id: createdUser.id,
        name: createdUser.name,
        email: createdUser.email,
      });
    });

    it('should throw an error if the email already exists', async () => {
      // Arrange
      const userData = {
        name: 'Test User',
        email: 'existing@example.com',
        password: 'Password123!',
      };
      const existingUser = {
        id: '1',
        name: 'Existing User',
        email: userData.email,
        password: 'hashedPassword',
        created: new Date().toISOString(),
      };

      userRepository.findByEmail.mockResolvedValue(existingUser);

      // Act & Assert
      await expect(authService.registerUser(userData)).rejects.toThrow(
        'Ein Benutzer mit dieser E-Mail-Adresse existiert bereits',
      );
      expect(userRepository.findByEmail).toHaveBeenCalledWith(userData.email);
      expect(userRepository.createUser).not.toHaveBeenCalled();
    });
  });

  describe('loginUser', () => {
    it('should return a token if credentials are valid', async () => {
      // Arrange
      const loginData = {
        email: 'test@example.com',
        password: 'Password123!',
      };
      const foundUser = {
        id: '1',
        name: 'Test User',
        email: loginData.email,
        password: 'hashedPassword',
        created: new Date().toISOString(),
      };
      const token = 'jwt.token.here';

      userRepository.findByEmail.mockResolvedValue(foundUser);
      (bcrypt.compare as jest.Mock).mockResolvedValue(true);
      jwtService.generateToken.mockReturnValue(token);

      // Act
      const result = await authService.loginUser(loginData);

      // Assert
      expect(userRepository.findByEmail).toHaveBeenCalledWith(loginData.email);
      expect(bcrypt.compare).toHaveBeenCalledWith(loginData.password, foundUser.password);
      expect(jwtService.generateToken).toHaveBeenCalledWith({ 
        userId: foundUser.id, 
        email: foundUser.email 
      });
      expect(result).toEqual({
        token,
        user: {
          id: foundUser.id,
          name: foundUser.name,
          email: foundUser.email,
        },
      });
    });

    it('should throw an error if the user does not exist', async () => {
      // Arrange
      const loginData = {
        email: 'nonexistent@example.com',
        password: 'Password123!',
      };

      userRepository.findByEmail.mockResolvedValue(null);

      // Act & Assert
      await expect(authService.loginUser(loginData)).rejects.toThrow(
        'Ungültige E-Mail-Adresse oder Passwort',
      );
      expect(userRepository.findByEmail).toHaveBeenCalledWith(loginData.email);
      expect(bcrypt.compare).not.toHaveBeenCalled();
    });

    it('should throw an error if the password is invalid', async () => {
      // Arrange
      const loginData = {
        email: 'test@example.com',
        password: 'WrongPassword',
      };
      const foundUser = {
        id: '1',
        name: 'Test User',
        email: loginData.email,
        password: 'hashedPassword',
        created: new Date().toISOString(),
      };

      userRepository.findByEmail.mockResolvedValue(foundUser);
      (bcrypt.compare as jest.Mock).mockResolvedValue(false);

      // Act & Assert
      await expect(authService.loginUser(loginData)).rejects.toThrow(
        'Ungültige E-Mail-Adresse oder Passwort',
      );
      expect(userRepository.findByEmail).toHaveBeenCalledWith(loginData.email);
      expect(bcrypt.compare).toHaveBeenCalledWith(loginData.password, foundUser.password);
      expect(jwtService.generateToken).not.toHaveBeenCalled();
    });
  });
});
