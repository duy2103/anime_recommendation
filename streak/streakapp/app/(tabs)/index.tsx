import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';

export default function HomeScreen() {
  const router = useRouter();
  return (
    <View style={styles.container}>
      <Image source={require('@/assets/images/partial-react-logo.png')} style={styles.logo} />
      <Text style={styles.title}>Welcome to Streak!</Text>
      <Text style={styles.subtitle}>Build healthy habits, track your progress, and never break your streak again.</Text>
      <TouchableOpacity style={styles.ctaBtn} onPress={() => router.push('/(tabs)/streaks')}>
        <Text style={styles.ctaBtnText}>View My Streaks</Text>
      </TouchableOpacity>
      <Text style={styles.tip}>Tip: Tap the + button to create your first streak!</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 32, backgroundColor: '#f8fafc' },
  logo: { width: 180, height: 110, marginBottom: 24, resizeMode: 'contain' },
  title: { fontSize: 28, fontWeight: 'bold', color: '#0a7ea4', marginBottom: 8 },
  subtitle: { fontSize: 16, color: '#333', textAlign: 'center', marginBottom: 24 },
  ctaBtn: { backgroundColor: '#0a7ea4', borderRadius: 8, paddingVertical: 14, paddingHorizontal: 32, marginBottom: 16 },
  ctaBtnText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
  tip: { color: '#888', fontSize: 14, marginTop: 12, textAlign: 'center' },
});
