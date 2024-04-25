import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { Link, Redirect } from 'expo-router';
import SignIn from './(auth)/sign-in'; // Import your SignIn component
import { useGlobalContext } from "../context/GlobalProvider";
import OnboardingTabs from './(onboarding)/onboarding-tabs';

export default function App() {

  const { loading, isLogged } = useGlobalContext();

  // if (!loading && isLogged) return <Redirect href="/home" />;
  
  return (
    <OnboardingTabs />
    // <SignIn />
  );
}

