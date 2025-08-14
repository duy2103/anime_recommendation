import { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import { getStreaks, getStreakCompletions, Streak } from '@/utils/streaks';

function getToday() {
  return new Date().toISOString().slice(0, 10);
}

function calcStats(streak: Streak, completions: { date: string }[]) {
  if (!completions.length) return { current: 0, longest: 0, rate: 0 };
  // Sort dates ascending
  const dates = completions.map(c => c.date).sort();
  let current = 1, longest = 1, streaking = 1;
  for (let i = 1; i < dates.length; i++) {
    const prev = new Date(dates[i - 1]);
    const curr = new Date(dates[i]);
    const diff = (curr.getTime() - prev.getTime()) / (1000 * 60 * 60 * 24);
    if (diff === 1) {
      streaking++;
      if (streaking > longest) longest = streaking;
    } else {
      streaking = 1;
    }
  }
  // Check if today is included for current streak
  const lastDate = dates[dates.length - 1];
  const today = getToday();
  if (lastDate === today) current = streaking;
  else current = 0;
  // Completion rate: completions / expected (approximate for demo)
  const created = streak.createdAt ? new Date(streak.createdAt) : new Date(dates[0]);
  const days = Math.max(1, (new Date(today).getTime() - created.getTime()) / (1000 * 60 * 60 * 24) + 1);
  const rate = completions.length / days;
  return { current, longest, rate: Math.round(rate * 100) / 100 };
}

export default function StreakStatsScreen({ streakId }: { streakId: number }) {
  const [streak, setStreak] = useState<Streak | null>(null);
  const [completions, setCompletions] = useState<{ date: string }[]>([]);

  useEffect(() => {
    getStreaks().then(list => setStreak(list.find(s => s.id === streakId) || null));
    getStreakCompletions(streakId).then(setCompletions);
  }, [streakId]);

  if (!streak) return <Text>Loading...</Text>;
  const stats = calcStats(streak, completions);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Stats for {streak.title}</Text>
      <Text>Current streak: {stats.current} days</Text>
      <Text>Longest streak: {stats.longest} days</Text>
      <Text>Completion rate: {stats.rate * 100}%</Text>
      <Text style={styles.section}>Completion Calendar:</Text>
      <FlatList
        data={completions}
        keyExtractor={item => item.date}
        numColumns={7}
        renderItem={({ item }) => (
          <View style={styles.dayCell}><Text style={styles.dayDone}>✓</Text></View>
        )}
        ListEmptyComponent={<Text>No completions yet.</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24 },
  title: { fontSize: 20, fontWeight: 'bold', marginBottom: 8 },
  section: { fontWeight: 'bold', marginTop: 16, marginBottom: 8 },
  dayCell: { width: 32, height: 32, justifyContent: 'center', alignItems: 'center', borderWidth: 1, borderColor: '#eee', margin: 2, borderRadius: 6 },
  dayDone: { color: 'green', fontWeight: 'bold' },
});
