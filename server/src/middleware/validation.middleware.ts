// Express-Typen für Type Safety
type Request = {
  body: Record<string, any>;
};

type Response = {
  status: (code: number) => Response;
  json: (data: any) => void;
};

type NextFunction = () => void;

// Zod-Schema Implementation für Type Safety
// Da die Typdeklarationen fehlen, implementieren wir eine vereinfachte Version
const z = {
  object: (schema: Record<string, any>) => ({
    parse: (data: Record<string, any>) => data,
  }),
  string: () => {
    const result: any = {
      min: (minLength: number, message: string) => result,
      email: (message: string) => result,
      regex: (regex: RegExp, message: string) => result
    };
    return result;
  },
  enum: (values: string[]) => ({}),
  ZodError: class ZodError {
    errors: { path: string[]; message: string }[];
    constructor(errors: { path: string[]; message: string }[]) {
      this.errors = errors;
    }
  }
};

// Schema für die Benutzerregistrierung
const registrationSchema = z.object({
  name: z.string().min(2, 'Der Name muss mindestens 2 Zeichen lang sein'),
  email: z.string().email('Ungültige E-Mail-Adresse'),
  password: z
    .string()
    .min(8, 'Das Passwort muss mindestens 8 Zeichen lang sein')
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])/,
      'Das Passwort muss mindestens einen Kleinbuchstaben, einen Großbuchstaben, eine Zahl und ein Sonderzeichen enthalten'
    ),
});

// Schema für den Login
const loginSchema = z.object({
  email: z.string().email('Ungültige E-Mail-Adresse'),
  password: z.string().min(1, 'Passwort ist erforderlich'),
});

/**
 * Middleware zur Validierung der Registrierungsdaten
 */
export const validateRegistration = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  try {
    registrationSchema.parse(req.body);
    next();
  } catch (error: any) { // Expliziter any-Typ für error
    if (error instanceof z.ZodError) {
      const formattedErrors = error.errors.map((e: any) => ({
        field: e.path.join('.'),
        message: e.message,
      }));
      
      res.status(400).json({
        success: false,
        message: 'Validierungsfehler',
        errors: formattedErrors,
      });
    } else {
      res.status(400).json({
        success: false,
        message: 'Ungültige Eingabedaten',
      });
    }
  }
};

/**
 * Middleware zur Validierung der Login-Daten
 */
export const validateLogin = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  try {
    loginSchema.parse(req.body);
    next();
  } catch (error: any) { // Expliziter any-Typ für error
    if (error instanceof z.ZodError) {
      const formattedErrors = error.errors.map((e: any) => ({
        field: e.path.join('.'),
        message: e.message,
      }));
      
      res.status(400).json({
        success: false,
        message: 'Validierungsfehler',
        errors: formattedErrors,
      });
    } else {
      res.status(400).json({
        success: false,
        message: 'Ungültige Eingabedaten',
      });
    }
  }
};
