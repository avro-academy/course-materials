import { useEffect, useState } from "react";

/** Like useState, but remembers the value in the browser between visits. */
export function useLocalStorage<T>(key: string, initialValue: () => T) {
  const [value, setValue] = useState<T>(() => {
    try {
      const saved = localStorage.getItem(key);
      return saved !== null ? (JSON.parse(saved) as T) : initialValue();
    } catch {
      return initialValue(); // broken or blocked storage: start fresh
    }
  });

  // After every render where the value changed, save it.
  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch {
      // Storage can be full or switched off (e.g. some private windows). The app still works, it just won't remember.
    }
  }, [key, value]);

  return [value, setValue] as const;
}
