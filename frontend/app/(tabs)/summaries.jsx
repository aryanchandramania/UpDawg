import { useState, useEffect } from 'react';
import { SafeAreaView } from 'react-native-safe-area-context'
import { View, Text, ScrollView, Dimensions, Alert, Image, Picker, TouchableOpacity } from "react-native";
import { StatusBar } from 'expo-status-bar';
import { images } from '../../constants';
import CustomButton from '../../components/CustomButton';
// import { Picker } from 'react-native-picker/picker';
import { SelectList } from 'react-native-dropdown-select-list'
import { Link, router } from "expo-router";
import { useGlobalContext } from '../../context/GlobalProvider';
// import { getHello } from "../../lib/appwrite";

const Summaries = () => {

  // make 5 boxes which are clickable and these boxes will be the summaries of the user's data

  // useEffect(() => {
  //   getHello();
  // }
  // , []);

  const summaries = [
    { id: 1, title: 'Summary 1', content: "The sun peeked over the horizon, casting a warm golden glow across the dewy meadow. Delicate wildflowers danced in the gentle morning breeze, their vibrant petals a kaleidoscope of colors. Nearby, a babbling brook trickled over mossy rocks, its soothing melody filling the air. In the distance, majestic snow-capped mountains stood as silent sentinels, their peaks piercing the azure sky. A lone deer grazed peacefully, occasionally lifting its head to survey its idyllic surroundings. Nature's grandeur was on full display, a serene and rejuvenating scene that reminded all who witnessed it of the simple yet profound beauty that exists in the world."},
    { id: 2, title: 'Summary 2', content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.' },
    { id: 3, title: 'Summary 3', content: 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.' },
    { id: 4, title: 'Summary 4', content: 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.' },
    { id: 5, title: 'Summary 5', content: 'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' },
  ];

  const [expandedSummaries, setExpandedSummaries] = useState({});

  // Function to handle click on summary
  const handleSummaryClick = (summaryId) => {
    setExpandedSummaries({ ...expandedSummaries, [summaryId]: !expandedSummaries[summaryId] });
  };

  return (
    <SafeAreaView classname="h-full">
      <ScrollView>
        <View className="bg-primary w-full flex min-h-[5vh] px-4 my-6 items-center mb-8">
          <Image
                source={images.logo}
                resizeMode="contain"
                className="w-[120px] h-[60px] absolute top-0"
          />
        </View>
        <View className="bg-primary w-full flex justify-center min-h-[75vh] px-4 my-6 items-center">

          {summaries.map(summary => (
            <TouchableOpacity
              key={summary.id}
              onPress={() => handleSummaryClick(summary.id)}
              style={{ backgroundColor: '#ebe7e1', borderRadius: 10, padding: 10, marginBottom: 14, width: '100%', maxWidth: 310 }}
            >
              <Text className="text-s font-psemibold mb-1">{summary.title}</Text>
              <Text className="text-s font-pregular">{expandedSummaries[summary.id] ? summary.content : summary.content.slice(0, 80) + '...'}</Text>
            </TouchableOpacity>
          ))}

        </View>
      </ScrollView>
    </SafeAreaView>
  )
}

export default Summaries