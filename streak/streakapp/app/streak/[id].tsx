import { View, Text, StyleSheet, Button, TouchableOpacity, ScrollView } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';

const dummyStreaks = [
  {
    id: 1,
    title: 'Drink Water',
    description: 'Stay hydrated every day',
    icon: '💧',
    color: '#00BFFF',
    frequency: 'daily',
    verificationType: 'manual',
    completions: ['2025-08-12', '2025-08-13', '2025-08-14'],
  },
  {
    id: 2,
    title: 'Read Book',
    description: 'Read 10 pages',
    icon: '📚',
    color: '#FFD700',
    frequency: 'daily',
    verificationType: 'manual',
    completions: ['2025-08-13'],
  },
];

function getToday() {
  return new Date().toISOString().slice(0, 10);
}

function getLastNDates(n: number) {
  const arr = [];
  const today = new Date();
  for (let i = n - 1; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(today.getDate() - i);
    arr.push(d.toISOString().slice(0, 10));
  }
  return arr;
}

export default function StreakDetailScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams();
  const streak = dummyStreaks.find(s => String(s.id) === String(id));
  if (!streak) return <Text>Streak not found.</Text>;

  // Calendar: last 14 days
  const days = getLastNDates(14);
  const completions = streak.completions || [];

  // Stats
  const currentStreak = completions.includes(getToday()) ? 1 : 0;
  const longestStreak = Math.max(currentStreak, completions.length);
  const completionRate = Math.round((completions.length / days.length) * 100);

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Button title="Back" onPress={() => router.back()} />
      <View style={[styles.header, { backgroundColor: streak.color + '22' }]}> 
        <Text style={styles.icon}>{streak.icon}</Text>
        <Text style={styles.title}>{streak.title}</Text>
      </View>
      <Text style={styles.desc}>{streak.description}</Text>
      <View style={styles.statsRow}>
        <View style={styles.stat}><Text style={styles.statNum}>{currentStreak}</Text><Text style={styles.statLabel}>Current</Text></View>
        <View style={styles.stat}><Text style={styles.statNum}>{longestStreak}</Text><Text style={styles.statLabel}>Longest</Text></View>
        <View style={styles.stat}><Text style={styles.statNum}>{completionRate}%</Text><Text style={styles.statLabel}>Rate</Text></View>
      </View>
      <Text style={styles.sectionTitle}>Last 2 Weeks</Text>
      <View style={styles.calendarRow}>
        {days.map(date => (
          <View key={date} style={[styles.dayCell, completions.includes(date) && styles.dayDone]}>
            <Text style={styles.dayText}>{date.slice(5)}</Text>
          </View>
        ))}
      </View>
      <TouchableOpacity style={styles.completeBtn}>
        <Text style={styles.completeBtnText}>Mark as Complete</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 24, gap: 12 },
  header: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 8, borderRadius: 12, padding: 16 },
  icon: { fontSize: 36 },
  title: { fontSize: 24, fontWeight: 'bold' },
  desc: { color: '#555', marginBottom: 8 },
  statsRow: { flexDirection: 'row', gap: 18, marginBottom: 8 },
  stat: { alignItems: 'center', flex: 1 },
  statNum: { fontSize: 20, fontWeight: 'bold', color: '#0a7ea4' },
  statLabel: { fontSize: 13, color: '#888' },
  sectionTitle: { fontWeight: 'bold', marginTop: 16, marginBottom: 8, fontSize: 16 },
  calendarRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 6, marginBottom: 16 },
  dayCell: { width: 44, height: 44, borderRadius: 8, backgroundColor: '#f2f2f2', justifyContent: 'center', alignItems: 'center' },
  dayDone: { backgroundColor: '#A1CEDC' },
  dayText: { fontSize: 13, color: '#333' },
  completeBtn: { backgroundColor: '#0a7ea4', borderRadius: 8, padding: 14, alignItems: 'center', marginTop: 12 },
  completeBtnText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
});
