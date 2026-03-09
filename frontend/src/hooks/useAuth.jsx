import { createContext, useContext, useEffect, useState } from "react";
import { api, tokenStorage } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => tokenStorage.get());
  const [user, setUser] = useState(null);
  const [isInitializing, setIsInitializing] = useState(true);

  useEffect(() => {
    async function bootstrap() {
      const storedToken = tokenStorage.get();

      if (!storedToken) {
        setIsInitializing(false);
        return;
      }

      try {
        const nextUser = await api.getCurrentUser();
        setToken(storedToken);
        setUser(nextUser);
      } catch (error) {
        tokenStorage.clear();
        setToken(null);
        setUser(null);
      } finally {
        setIsInitializing(false);
      }
    }

    bootstrap();
  }, []);

  async function login(credentials) {
    const tokenResponse = await api.login(credentials);
    tokenStorage.set(tokenResponse.access_token);
    setToken(tokenResponse.access_token);

    const nextUser = await api.getCurrentUser();
    setUser(nextUser);

    return nextUser;
  }

  function logout() {
    tokenStorage.clear();
    setToken(null);
    setUser(null);
  }

  async function refreshUser() {
    const nextUser = await api.getCurrentUser();
    setUser(nextUser);
    return nextUser;
  }

  const value = {
    token,
    user,
    isInitializing,
    isAuthenticated: Boolean(token),
    login,
    logout,
    refreshUser
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}
