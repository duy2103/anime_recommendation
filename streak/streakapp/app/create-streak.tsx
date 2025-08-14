import { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';

const COLORS = ['#00BFFF', '#FFD700', '#FF69B4', '#32CD32', '#FF6347', '#A1CEDC', '#A9A9F5'];
const EMOJIS = ['💧', '📚', '🏃‍♂️', '🧘‍♀️', '🍎', '📝', '🔥', '🌞', '🌱', '🎨'];

export default function CreateStreakScreen() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [icon, setIcon] = useState('');
  const [color, setColor] = useState(COLORS[0]);
  const [frequency, setFrequency] = useState('daily');
  const [verificationType, setVerificationType] = useState('manual');
  const router = useRouter();

  function handleSave() {
    // For frontend only, just go back to streaks and show the new streak at the top
    router.replace('/(tabs)/streaks?created=1');
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.sectionTitle}>Create a New Streak</Text>
      <Text style={styles.label}>Title *</Text>
      <TextInput style={styles.input} value={title} onChangeText={setTitle} placeholder="e.g. Drink Water" />
      <Text style={styles.label}>Description</Text>
      <TextInput style={styles.input} value={description} onChangeText={setDescription} placeholder="Optional" />
      <Text style={styles.label}>Icon (emoji)</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.emojiRow}>
        {EMOJIS.map(e => (
          <TouchableOpacity key={e} style={[styles.emojiBtn, icon === e && styles.emojiSelected]} onPress={() => setIcon(e)}>
            <Text style={styles.emoji}>{e}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
      <TextInput style={styles.input} value={icon} onChangeText={setIcon} placeholder="Or type your own emoji" />
      <Text style={styles.label}>Color</Text>
      <View style={styles.colorRow}>
        {COLORS.map(c => (
          <TouchableOpacity key={c} style={[styles.colorBtn, { backgroundColor: c }, color === c && styles.colorSelected]} onPress={() => setColor(c)} />
        ))}
      </View>
      <TextInput style={styles.input} value={color} onChangeText={setColor} placeholder="#00BFFF" />
      <Text style={styles.label}>Frequency</Text>
      <View style={styles.row}>
        {['daily', 'weekly', 'custom'].map(f => (
          <TouchableOpacity key={f} style={[styles.chip, frequency === f && styles.chipSelected]} onPress={() => setFrequency(f)}>
            <Text style={styles.chipText}>{f.charAt(0).toUpperCase() + f.slice(1)}</Text>
          </TouchableOpacity>
        ))}
      </View>
      <Text style={styles.label}>Verification</Text>
      <View style={styles.row}>
        {['manual', 'auto-health', 'webhook'].map(v => (
          <TouchableOpacity key={v} style={[styles.chip, verificationType === v && styles.chipSelected]} onPress={() => setVerificationType(v)}>
            <Text style={styles.chipText}>{v.replace('-', ' ')}</Text>
          </TouchableOpacity>
        ))}
      </View>
      <Button title={'Create Streak'} onPress={handleSave} disabled={!title} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 24, gap: 12 },
  sectionTitle: { fontSize: 22, fontWeight: 'bold', marginBottom: 12, textAlign: 'center' },
  label: { fontWeight: 'bold', marginTop: 8 },
  input: { borderWidth: 1, borderColor: '#ccc', borderRadius: 8, padding: 8, marginBottom: 4, backgroundColor: '#fff' },
  emojiRow: { flexDirection: 'row', marginBottom: 8 },
  emojiBtn: { padding: 8, borderRadius: 8, marginRight: 6, backgroundColor: '#f2f2f2' },
  emojiSelected: { backgroundColor: '#A1CEDC' },
  emoji: { fontSize: 28 },
  colorRow: { flexDirection: 'row', marginBottom: 8, marginTop: 4 },
  colorBtn: { width: 32, height: 32, borderRadius: 16, marginRight: 8, borderWidth: 2, borderColor: '#fff' },
  colorSelected: { borderColor: '#0a7ea4', borderWidth: 3 },
  row: { flexDirection: 'row', gap: 8, marginBottom: 8 },
  chip: { paddingHorizontal: 14, paddingVertical: 7, borderRadius: 16, borderWidth: 1, borderColor: '#ccc', marginRight: 8, backgroundColor: '#f8fafc' },
  chipSelected: { backgroundColor: '#A1CEDC', borderColor: '#0a7ea4' },
  chipText: { fontWeight: '500' },
});
