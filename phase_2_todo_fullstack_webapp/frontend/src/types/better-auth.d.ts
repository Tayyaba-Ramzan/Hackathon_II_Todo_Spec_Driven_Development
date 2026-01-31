declare module 'better-auth' {
  interface BetterAuthOptions {
    secret?: string;
    database?: {
      provider: string;
      url: string;
    };
    jwt?: {
      expiresIn: string;
    };
    [key: string]: any; // Allow additional properties
  }

  interface AuthClient {
    signIn: (provider: string, options?: any) => Promise<any>;
    signOut: () => Promise<void>;
    getSession: () => Promise<any>;
    // Add other methods as needed
  }

  export interface BetterAuthClient extends AuthClient {}

  export interface BetterAuth {
    (): any; // Default export function
    client: BetterAuthClient;
    // Add other exports as needed
  }

  export function betterAuth(options: BetterAuthOptions): BetterAuth;

  export default betterAuth;
}