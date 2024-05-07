import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { Link, Redirect } from 'expo-router';
import SignIn from './(auth)/sign-in'; // Import your SignIn component
import { useGlobalContext } from "../context/GlobalProvider";
import OnboardingTabs from './(onboarding)/onboarding-tabs';
import {NavigationContainer} from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

export default function App() {

  const { loading, isLogged } = useGlobalContext();

  if (!loading && isLogged) return <Redirect href="/home" />;
  
  return (
    // <OnboardingTabs />
    // <NavigationContainer>
      <SignIn />
    
  );
}


