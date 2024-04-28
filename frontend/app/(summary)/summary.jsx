import { useState, useEffect, Fragment } from 'react';
import { SafeAreaView } from 'react-native-safe-area-context'
import { View, Text, ScrollView, Dimensions, Alert, Image, Picker, TouchableOpacity, Animated } from "react-native";
import { StatusBar } from 'expo-status-bar';
import { images } from '../../constants';
import { icons } from '../../constants';
import CustomButton from '../../components/CustomButton';
// import { Picker } from 'react-native-picker/picker';
import { SelectList } from 'react-native-dropdown-select-list'
import { Link, router } from "expo-router";

const Summary = () => {

  // create a summary box which is a card with a title and a description

  const paragraph = "The sun peeked over the horizon, casting a warm golden glow across the dewy meadow. Delicate wildflowers danced in the gentle morning breeze, their vibrant petals a kaleidoscope of colors. Nearby, a babbling brook trickled over mossy rocks, its soothing melody filling the air. In the distance, majestic snow-capped mountains stood as silent sentinels, their peaks piercing the azure sky. A lone deer grazed peacefully, occasionally lifting its head to survey its idyllic surroundings. Nature's grandeur was on full display, a serene and rejuvenating scene that reminded all who witnessed it of the simple yet profound beauty that exists in the world. "

  const words = paragraph.split(' ');

  // State to manage displayed words
  const [displayedWords, setDisplayedWords] = useState([]);
  
  // Index of the current word being displayed
  const [currentWordIndex, setCurrentWordIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      if (currentWordIndex < words.length) {
        setDisplayedWords(words.slice(0, currentWordIndex + 1));
        setCurrentWordIndex(currentWordIndex + 1);
      } else {
        clearInterval(interval); // Stop when all words are displayed
      }
    }, 10); // Adjust the duration as needed

    return () => clearInterval(interval);
  }, [currentWordIndex]);

  return (
    <SafeAreaView classname="h-full">
      <ScrollView>
        <View className="bg-primary w-full flex min-h-[5vh] px-4 my-6 items-center mb-10">
        
        <TouchableOpacity className="absolute left-0"  onPress={() => router.replace('/home')}>
          <Image 
              source={icons.back}
              resizeMode="contain"
              className="w-[60px] h-[70px]"
          />
        </TouchableOpacity>

        <Image
              source={images.logo}
              resizeMode="contain"
              className="w-[120px] h-[60px] absolute top-0"
        />

        </View>
        <View className="bg-primary w-full flex min-h-[85vh] px-4 my-6 items-center">

        <View style={{ backgroundColor: '#ebe7e1', borderRadius: 10, padding: 13, marginBottom: 20 }}>
            {/* First Text */}
            <View style={{ marginBottom: 10 }}>
              <Text className="text-lg font-psemibold mb-4">
                Here's your summary for the last X days
              </Text>
              <Text className="text-s font-pregular">
                {displayedWords.join(' ')}
              </Text>
            </View>
        </View>

        </View>
      </ScrollView>
    </SafeAreaView>
  )
}

export default Summary