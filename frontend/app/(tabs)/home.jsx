import { useState, useEffect } from 'react';
import { SafeAreaView } from 'react-native-safe-area-context'
import { View, Text, ScrollView, Dimensions, Alert, Image, Picker } from "react-native";
import { StatusBar } from 'expo-status-bar';
import { images } from '../../constants';
import CustomButton from '../../components/CustomButton';
// import { Picker } from 'react-native-picker/picker';
import { SelectList } from 'react-native-dropdown-select-list'
import { Link, router, useRouter } from "expo-router";
import { useGlobalContext } from '../../context/GlobalProvider';

const Home = ( ) => {

  const [selected, setSelected] = useState("1");
  const [greeting, setGreeting] = useState("");
  const { user, days, setDays } = useGlobalContext();
  const route = useRouter();

  useEffect(() => {
    // Get the current time
    const currentTime = new Date().getHours();

    // Set greeting based on time
    if (currentTime >= 0 && currentTime < 12) {
      setGreeting("Good morning");
    } else if (currentTime >= 12 && currentTime < 18) {
      setGreeting("Good afternoon");
    } else {
      setGreeting("Good evening");
    }
  }, []);

  const data = [
    {key:'1', value:'1 day'},
    {key:'2', value:'2 days'},
    {key:'3', value:'3 days'},
    {key:'4', value:'4 days'},
    {key:'5', value:'5 days'},
    {key:'6', value:'6 days'},
    {key:'7', value:'7 days'},
]

  const handlePress = () => {
      // Alert.alert("Success", "User signed in successfully");
      const numericalValue = parseInt(selected);
      setDays(numericalValue);
      // console.log(days)
      router.replace('/summary');
      // navigation.navigate('Summary', { selectedValue: selected });
  }

  const capitalizeFirstLetter = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
  };

  return (

    <SafeAreaView classname="h-full">
      {/* <ScrollView> */}
        <View className="bg-primary w-full flex justify-center min-h-[85vh] px-4 my-6 items-center">

          <Image
            source={images.logo}
            resizeMode="contain"
            className="w-[120px] h-[60px] absolute top-0"
          />

          <Text className="text-xl font-psemibold text-#482A14 mt-5 mb-5">
            {greeting}, {user && user.username ? capitalizeFirstLetter(user.username) : ''}!
          </Text>

          <View className="w-full mb-4">
            <CustomButton
                title="What's Up, Dawg?"
                handlePress={handlePress}
                otherStyles="mt-6"
              />
          </View>

          <SelectList 
            setSelected={(val) => setSelected(val)} 
            data={data} 
            save="value"
            className="w-full"
          />

        </View>
      {/* </ScrollView> */}
    </SafeAreaView>


    
  )
}

export default Home