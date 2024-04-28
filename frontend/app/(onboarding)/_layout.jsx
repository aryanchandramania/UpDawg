import { Redirect, Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";

const OnboardingLayout = () => {
  return (
    <>
      <Stack>
        <Stack.Screen
          name="onboarding-tabs"
          options={{
            headerShown: false,
          }}
        />
      </Stack>
      
      {/* <StatusBar backgroundColor="#161622" style="light" /> */}
    </>
  )
}

export default OnboardingLayout
