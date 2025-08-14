import { View, Text, StyleSheet, ScrollView, Image } from 'react-native';

export default function ExploreScreen() {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Image source={require('@/assets/images/react-logo.png')} style={styles.logo} />
      <Text style={styles.title}>Explore Streak Features</Text>
      <Text style={styles.sectionTitle}>What you can do:</Text>
      <View style={styles.featureCard}>
        <Text style={styles.featureIcon}>🔥</Text>
        <Text style={styles.featureText}>Create and track daily, weekly, or custom streaks</Text>
      </View>
      <View style={styles.featureCard}>
        <Text style={styles.featureIcon}>📅</Text>
        <Text style={styles.featureText}>Visualize your progress with a calendar view</Text>
      </View>
      <View style={styles.featureCard}>
        <Text style={styles.featureIcon}>⏰</Text>
        <Text style={styles.featureText}>Set reminders so you never miss a day</Text>
      </View>
      <View style={styles.featureCard}>
        <Text style={styles.featureIcon}>🔒</Text>
        <Text style={styles.featureText}>Sync and secure your streaks (coming soon!)</Text>
      </View>
      <Text style={styles.sectionTitle}>How to get started:</Text>
      <Text style={styles.step}>1. Tap the + button to create your first streak</Text>
      <Text style={styles.step}>2. Mark your streaks as complete each day</Text>
      <Text style={styles.step}>3. Watch your progress grow!</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 28, alignItems: 'center', backgroundColor: '#f8fafc' },
  logo: { width: 120, height: 120, marginBottom: 18, resizeMode: 'contain' },
  title: { fontSize: 24, fontWeight: 'bold', color: '#0a7ea4', marginBottom: 18 },
  sectionTitle: { fontWeight: 'bold', fontSize: 16, marginTop: 18, marginBottom: 8, color: '#222' },
  featureCard: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, width: '100%', shadowColor: '#000', shadowOpacity: 0.06, shadowRadius: 8, shadowOffset: { width: 0, height: 2 }, elevation: 2 },
  featureIcon: { fontSize: 24, marginRight: 12 },
  featureText: { fontSize: 15, color: '#333', flex: 1 },
  step: { fontSize: 15, color: '#444', marginBottom: 4, alignSelf: 'flex-start' },
});
