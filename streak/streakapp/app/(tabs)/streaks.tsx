import { View, Text, FlatList, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { Link, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams } from 'expo-router';
import { useState, useEffect } from 'react';

const dummyStreaks = [
  {
    id: 1,
    title: 'Drink Water',
    description: 'Stay hydrated every day',
    icon: '💧',
    color: '#00BFFF',
    frequency: 'daily',
    verificationType: 'manual',
  },
  {
    id: 2,
    title: 'Read Book',
    description: 'Read 10 pages',
    icon: '📚',
    color: '#FFD700',
    frequency: 'daily',
    verificationType: 'manual',
  },
];

export default function StreakListScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const [showCreated, setShowCreated] = useState(false);

  useEffect(() => {
    if (params.created) {
      setShowCreated(true);
      setTimeout(() => setShowCreated(false), 2000);
    }
  }, [params.created]);

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#f8fafc' }}>
      <View style={styles.header}>
        <Text style={styles.title}>My Streaks</Text>
      </View>
      <FlatList
        data={dummyStreaks}
        keyExtractor={item => String(item.id)}
        contentContainerStyle={{ padding: 16, paddingBottom: 100 }}
        renderItem={({ item }) => (
          <Link href={{ pathname: '/streak/[id]', params: { id: String(item.id) } }} asChild>
            <TouchableOpacity style={[styles.card, { borderLeftColor: item.color || '#0a7ea4' }]}> 
              <View style={styles.cardHeader}>
                <Text style={styles.cardIcon}>{item.icon || '🔥'}</Text>
                <Text style={styles.cardTitle}>{item.title}</Text>
              </View>
              <Text style={styles.cardDesc}>{item.description}</Text>
              <View style={styles.cardMetaRow}>
                <Text style={styles.cardMeta}>{item.frequency}</Text>
                <Text style={styles.cardMeta}>{item.verificationType}</Text>
              </View>
            </TouchableOpacity>
          </Link>
        )}
        ListEmptyComponent={<Text style={styles.empty}>No streaks yet. Tap + to create one!</Text>}
      />
      {showCreated && (
        <View style={styles.toast}><Text style={styles.toastText}>Streak created!</Text></View>
      )}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => router.push('/create-streak')}
        activeOpacity={0.85}
      >
        <Ionicons name="add" size={32} color="#fff" />
      </TouchableOpacity>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  header: { flexDirection: 'row', justifyContent: 'center', alignItems: 'center', paddingTop: 24, paddingBottom: 8, backgroundColor: '#f8fafc' },
  title: { fontSize: 28, fontWeight: 'bold', color: '#222' },
  card: { backgroundColor: '#fff', borderRadius: 16, padding: 20, marginBottom: 16, borderLeftWidth: 6, shadowColor: '#000', shadowOpacity: 0.06, shadowRadius: 8, shadowOffset: { width: 0, height: 2 }, elevation: 2 },
  cardHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: 6 },
  cardIcon: { fontSize: 28, marginRight: 10 },
  cardTitle: { fontSize: 20, fontWeight: 'bold', color: '#222' },
  cardDesc: { color: '#555', marginBottom: 8, marginTop: 2 },
  cardMetaRow: { flexDirection: 'row', gap: 12 },
  cardMeta: { fontSize: 13, color: '#888', marginRight: 12 },
  fab: { position: 'absolute', right: 24, bottom: 36, backgroundColor: '#0a7ea4', borderRadius: 32, width: 56, height: 56, justifyContent: 'center', alignItems: 'center', shadowColor: '#000', shadowOpacity: 0.18, shadowRadius: 8, shadowOffset: { width: 0, height: 4 }, elevation: 4 },
  empty: { textAlign: 'center', color: '#888', marginTop: 40, fontSize: 16 },
  toast: { position: 'absolute', top: 60, left: 0, right: 0, alignItems: 'center', zIndex: 10 },
  toastText: { backgroundColor: '#0a7ea4', color: '#fff', paddingHorizontal: 18, paddingVertical: 10, borderRadius: 20, fontWeight: 'bold', fontSize: 16, overflow: 'hidden' },
});
