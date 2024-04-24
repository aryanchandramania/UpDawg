import { useState } from 'react';
import { SafeAreaView } from 'react-native-safe-area-context'
import { View, Text, ScrollView, Dimensions, Alert, Image, Picker } from "react-native";
import { StatusBar } from 'expo-status-bar';
import { images } from '../../constants';
import CustomButton from '../../components/CustomButton';
// import { Picker } from 'react-native-picker/picker';
import { SelectList } from 'react-native-dropdown-select-list'

const Home = () => {

  const [selected, setSelected] = useState("");

  const data = [
    {key:'1', value:'1 day'},
    {key:'2', value:'2 days'},
    {key:'3', value:'3 days'},
    {key:'4', value:'4 days'},
    {key:'5', value:'5 days'},
    {key:'6', value:'6 days'},
    {key:'7', value:'7 days'},
]

  return (
    // put some text in the center of screen saying Hello (get username) and center the text too
    // on top of the screen put a logo of your choice and center the image too
    // also make a button that says What's UpDawg
    // Also have a dropdown menu beside the button on the right side with 1-7 days options

    <SafeAreaView classname="h-full">
      {/* <ScrollView> */}
        <View className="bg-primary w-full flex justify-center min-h-[85vh] px-4 my-6 items-center">

          <Image
            source={images.logo}
            resizeMode="contain"
            className="w-[120px] h-[60px] absolute top-0"
          />

          <Text className="text-3xl font-semibold text-#482A14 mt-5 mb-5 font-psemibold">
            Hello, Shash!
          </Text>

          <View className="w-full mb-4">
            <CustomButton
                title="What's Up, Dawg?"
                onPress={() => Alert.alert("What's Up, Dawg?")}
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