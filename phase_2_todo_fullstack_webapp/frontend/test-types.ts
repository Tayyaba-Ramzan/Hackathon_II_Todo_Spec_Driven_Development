// Simple test to verify better-auth types work
import { betterAuth } from "better-auth";

const auth = betterAuth({
  secret: "test-secret",
  database: {
    provider: "sqlite",
    url: "sqlite::memory:",
  },
  jwt: {
    expiresIn: '7d',
  },
});

console.log("Auth initialized:", !!auth);