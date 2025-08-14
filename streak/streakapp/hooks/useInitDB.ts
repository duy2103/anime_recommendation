import { useEffect } from 'react';
import { initDB } from '@/utils/streaks';

export function useInitDB() {
  useEffect(() => {
    initDB();
  }, []);
}
