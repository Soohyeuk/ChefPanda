import React from 'react';
import { Link, Stack } from 'expo-router';
import { StyleSheet, Text } from 'react-native';

export default function NotFoundScreen() {
  return (
    <>
      <Stack.Screen options={{ title: 'Oops!' }} />
      <Text style={styles.container}>
        <Text style={{ fontSize: 20, marginBottom: 10 }}>This screen does not exist.</Text>
        <Link href="/" style={styles.link}>
          <Text style={{ fontSize: 16, color: 'blue' }}>Go to home screen!</Text>
        </Link>
      </Text>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  link: {
    marginTop: 15,
    paddingVertical: 15,
  },
});
