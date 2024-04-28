import { Redirect, Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";

const SummaryLayout = () => {
  return (
    <>
      <Stack>
        <Stack.Screen
          name="summary"
          options={{
            headerShown: false,
          }}
        />
      </Stack>
      
      {/* <StatusBar backgroundColor="#161622" style="light" /> */}
    </>
  )
}

export default SummaryLayout
