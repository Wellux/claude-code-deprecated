// Express-Typen als Mock (solange die Typdeklarationen fehlen)
type Router = {
  post: (path: string, ...handlers: any[]) => Router;
  get: (path: string, ...handlers: any[]) => Router;
};

type Request = {
  body: Record<string, any>;
  user?: {
    userId: string;
    email: string;
  };
};

type Response = {
  status: (code: number) => Response;
  json: (data: any) => void;
};

// Import der Controller und Middleware
import { AuthController } from '../controllers/auth.controller';
import { AuthMiddleware } from '../middleware/auth.middleware';

// Mock für die Validierungs-Middleware, da diese nicht importiert werden kann
const validateRegistration = (req: Request, res: Response, next: () => void) => next();
const validateLogin = (req: Request, res: Response, next: () => void) => next();

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
 * Konfiguriert die Authentifizierungs-Routen
 */
export const configureAuthRoutes = (
  router: Router,
  authController: AuthController,
  authMiddleware: AuthMiddleware
): Router => {
  // Öffentliche Routen
  router.post('/register', validateRegistration, (req: Request, res: Response) => authController.register(req, res));
  router.post('/login', validateLogin, (req: Request, res: Response) => authController.login(req, res));
  router.post('/logout', (req: Request, res: Response) => authController.logout(req, res));

  // Geschützte Route zum Testen der Authentifizierung
  router.get('/me', authMiddleware.authenticate, (req: Request, res: Response) => {
    res.status(200).json({
      success: true,
      message: 'Authentifizierter Benutzer',
      data: {
        userId: req.user?.userId,
        email: req.user?.email,
      },
    });
  });

  return router;
};
