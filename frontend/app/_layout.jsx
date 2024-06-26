import { StyleSheet, Text, View } from 'react-native'
import { useEffect } from 'react'
import { Slot, SplashScreen, Stack } from 'expo-router'; 
import { useFonts } from 'expo-font';

import GlobalProvider from '../context/GlobalProvider';
import { useGlobalContext } from "../context/GlobalProvider";
import {NavigationContainer} from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { SignIn } from './(auth)/sign-in';
import { Home } from './(tabs)/home';
import { Summary } from './(summary)/summary';
import { OnboardingTabs } from './(onboarding)/onboarding-tabs';
import { App } from './index';

SplashScreen.preventAutoHideAsync();

// const Stack = createNativeStackNavigator();


const RootLayout = () => {

    const [fontsLoaded, error] = useFonts({
        "Poppins-Black": require("../assets/fonts/Poppins-Black.ttf"),
        "Poppins-Bold": require("../assets/fonts/Poppins-Bold.ttf"),
        "Poppins-ExtraBold": require("../assets/fonts/Poppins-ExtraBold.ttf"),
        "Poppins-ExtraLight": require("../assets/fonts/Poppins-ExtraLight.ttf"),
        "Poppins-Light": require("../assets/fonts/Poppins-Light.ttf"),
        "Poppins-Medium": require("../assets/fonts/Poppins-Medium.ttf"),
        "Poppins-Regular": require("../assets/fonts/Poppins-Regular.ttf"),
        "Poppins-SemiBold": require("../assets/fonts/Poppins-SemiBold.ttf"),
        "Poppins-Thin": require("../assets/fonts/Poppins-Thin.ttf"),
      });
    
      useEffect(() => {
        if (error) throw error;
    
        if (fontsLoaded) {
          SplashScreen.hideAsync();
        }
      }, [fontsLoaded, error]);
    
      if (!fontsLoaded) {
        return null;
      }
    
      if (!fontsLoaded && !error) {
        return null;
      }  

  return (
    
    <GlobalProvider>
      <Stack>
          <Stack.Screen name="index" options={{ headerShown: false}} />
          <Stack.Screen name="(auth)" options={{ headerShown: false}}  />
          <Stack.Screen name="(tabs)" options={{ headerShown: false}} />
          <Stack.Screen name="(onboarding)" options={{ headerShown: false}} />
          <Stack.Screen name="(summary)" options={{ headerShown: false}} />
      </Stack>
    </GlobalProvider>
    
  )
}

export default RootLayout
