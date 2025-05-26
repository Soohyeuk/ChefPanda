import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { useFonts } from 'expo-font';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useColorScheme } from 'react-native';
import 'react-native-reanimated';
import { useEffect, useState } from 'react';
import { View } from 'react-native';
import '../global.css';
import ChefPanda from '../assets/images/chef_panda.svg';

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [loaded] = useFonts({
    SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
  });

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading time - replace with actual initialization logic
    setTimeout(() => {
      setIsLoading(false);
    }, 2000);
  }, []);

  if (!loaded) {
    // Async font loading only occurs in development.
    return null;
  }

  if (isLoading) {
    return (
      <View className="flex-1 items-center justify-center bg-primary">
        <ChefPanda width={225} height={216} />
      </View>
    );
  }

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="+not-found" options={{ headerShown: false }} />
      </Stack>
      <StatusBar style="auto" />
    </ThemeProvider>
  );
}
