import * as Notifications from 'expo-notifications';
import { useEffect } from 'react';

export async function scheduleStreakReminder(hour: number, minute: number, streakTitle: string) {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: 'Streak Reminder',
      body: `Don't forget to complete: ${streakTitle}`,
    },
    trigger: {
      hour,
      minute,
      repeats: true,
    },
  });
}

export function useNotificationSetup() {
  useEffect(() => {
    Notifications.requestPermissionsAsync();
  }, []);
}
