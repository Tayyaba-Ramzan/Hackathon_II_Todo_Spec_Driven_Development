declare module 'better-auth' {
  export interface AuthConfig {
    secret?: string;
    database?: {
      provider: string;
      url: string;
    };
    jwt?: {
      expiresIn: string;
    };
    [key: string]: any;
  }

  export interface BetterAuthClient {
    signIn: (provider: string, options?: any) => Promise<any>;
    signOut: () => Promise<void>;
    getSession: () => Promise<any>;
  }

  export interface BetterAuthInstance {
    client: BetterAuthClient;
  }

  export function betterAuth(config: AuthConfig): BetterAuthInstance;
}