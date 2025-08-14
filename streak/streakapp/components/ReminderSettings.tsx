import { useState } from 'react';
import { View, Text, Button, StyleSheet, Platform } from 'react-native';
import { scheduleStreakReminder } from '@/utils/reminders';

export default function ReminderSettings({ streakTitle }: { streakTitle: string }) {
  const [hour, setHour] = useState(9);
  const [minute, setMinute] = useState(0);
  const [scheduled, setScheduled] = useState(false);

  async function handleSchedule() {
    await scheduleStreakReminder(hour, minute, streakTitle);
    setScheduled(true);
  }

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Set daily reminder time:</Text>
      <View style={styles.row}>
        <Button title="-" onPress={() => setHour(h => Math.max(0, h - 1))} />
        <Text style={styles.time}>{hour.toString().padStart(2, '0')}</Text>
        <Button title="+" onPress={() => setHour(h => Math.min(23, h + 1))} />
        <Text>:</Text>
        <Button title="-" onPress={() => setMinute(m => Math.max(0, m - 1))} />
        <Text style={styles.time}>{minute.toString().padStart(2, '0')}</Text>
        <Button title="+" onPress={() => setMinute(m => Math.min(59, m + 1))} />
      </View>
      <Button title={scheduled ? 'Reminder Set!' : 'Set Reminder'} onPress={handleSchedule} />
      {Platform.OS === 'ios' && <Text style={styles.note}>Make sure notifications are enabled in Settings.</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginTop: 16, marginBottom: 16 },
  label: { fontWeight: 'bold', marginBottom: 8 },
  row: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  time: { fontSize: 18, fontWeight: 'bold', marginHorizontal: 4 },
  note: { color: '#888', marginTop: 8 },
});
