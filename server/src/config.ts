import dotenv from 'dotenv';
import { z } from 'zod';

// Lade Umgebungsvariablen aus .env-Datei (falls vorhanden)
dotenv.config();

// Schema für die Validierung der Umgebungsvariablen
const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.string().transform(val => parseInt(val, 10)).default('3000'),
  JWT_SECRET: z.string().min(32).default('replace_this_with_a_secure_secret_in_production_at_least_32_chars'),
  JWT_EXPIRES_IN: z.string().default('1d'),
  CORS_ORIGIN: z.string().default('*'),
});

// Validiere Umgebungsvariablen und setze Standardwerte, falls erforderlich
const env = envSchema.parse(process.env);

export const config = {
  env: env.NODE_ENV,
  server: {
    port: env.PORT,
  },
  jwt: {
    secret: env.JWT_SECRET,
    expiresIn: env.JWT_EXPIRES_IN,
  },
  cors: {
    origin: env.CORS_ORIGIN,
  },
};
