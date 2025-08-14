import * as SQLite from 'expo-sqlite';

const db = SQLite.openDatabase('streaks.db');

export type Frequency = 'daily' | 'weekly' | 'custom';
export type VerificationType = 'manual' | 'auto-health' | 'webhook';

export interface Streak {
  id?: number;
  title: string;
  description?: string;
  icon?: string;
  color?: string;
  frequency: Frequency;
  customDays?: number[]; // 0=Sun, 1=Mon, ...
  verificationType: VerificationType;
  createdAt?: string;
}

export interface StreakCompletion {
  id?: number;
  streakId: number;
  date: string; // YYYY-MM-DD
}

export function initDB() {
  db.transaction(tx => {
    tx.executeSql(
      `CREATE TABLE IF NOT EXISTS streaks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        icon TEXT,
        color TEXT,
        frequency TEXT NOT NULL,
        customDays TEXT,
        verificationType TEXT NOT NULL,
        createdAt TEXT DEFAULT (datetime('now'))
      );`
    );
    tx.executeSql(
      `CREATE TABLE IF NOT EXISTS streakCompletions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        streakId INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(streakId) REFERENCES streaks(id)
      );`
    );
  });
}

export function createStreak(streak: Streak): Promise<number> {
  return new Promise((resolve, reject) => {
    db.transaction(tx => {
      tx.executeSql(
        `INSERT INTO streaks (title, description, icon, color, frequency, customDays, verificationType) VALUES (?, ?, ?, ?, ?, ?, ?);`,
        [
          streak.title,
          streak.description ?? null,
          streak.icon ?? null,
          streak.color ?? null,
          streak.frequency,
          streak.customDays ? JSON.stringify(streak.customDays) : null,
          streak.verificationType,
        ],
        (_, result) => resolve(result.insertId as number),
        (_, error) => { reject(error); return false; }
      );
    });
  });
}

export function getStreaks(): Promise<Streak[]> {
  return new Promise((resolve, reject) => {
    db.transaction(tx => {
      tx.executeSql(
        `SELECT * FROM streaks;`,
        [],
        (_, { rows }) => {
          const data = rows._array.map(row => ({
            ...row,
            customDays: row.customDays ? JSON.parse(row.customDays) : undefined,
          }));
          resolve(data);
        },
        (_, error) => { reject(error); return false; }
      );
    });
  });
}

export function markStreakComplete(streakId: number, date: string): Promise<void> {
  return new Promise((resolve, reject) => {
    db.transaction(tx => {
      tx.executeSql(
        `INSERT INTO streakCompletions (streakId, date) VALUES (?, ?);`,
        [streakId, date],
        () => resolve(),
        (_, error) => { reject(error); return false; }
      );
    });
  });
}

export function getStreakCompletions(streakId: number): Promise<StreakCompletion[]> {
  return new Promise((resolve, reject) => {
    db.transaction(tx => {
      tx.executeSql(
        `SELECT * FROM streakCompletions WHERE streakId = ?;`,
        [streakId],
        (_, { rows }) => resolve(rows._array),
        (_, error) => { reject(error); return false; }
      );
    });
  });
}
