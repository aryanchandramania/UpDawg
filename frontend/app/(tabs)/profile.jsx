import { useState } from "react";
import { Link, router } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { View, Text, ScrollView, Dimensions, Alert, Image, TouchableOpacity } from "react-native";

import { images } from '../../constants';
import CustomButton from '../../components/CustomButton';
import { useGlobalContext } from "../../context/GlobalProvider";
import { icons } from "../../constants";
import { signOut } from "../../lib/appwrite";

const Profile = () => {
  const { user, setUser, setIsLogged } = useGlobalContext();

  const logout = async () => {
    await signOut();
    setUser(null);
    setIsLogged(false);

    router.replace("/sign-in");
  };

  return (
    
    <SafeAreaView classname="bg-primary h-full">
      
        <View className="w-full flex justify-center min-h-[85vh] px-4 my-6">

          <Image
            source={images.logo}
            resizeMode="contain"
            className="w-[120px] h-[60px]"
          />

          {/* <Text className="text-xl font-semibold text-#482A14 mt-5 font-psemibold">
            {user.username}
          </Text>
          <Text className="text-xl font-semibold text-#482A14 mt-5 font-psemibold">
            {user.email}
          </Text> */}

          <TouchableOpacity
              onPress={logout}
              className="flex w-full items-end mb-10"
            >
              <Image
                source={icons.logout}
                resizeMode="contain"
                className="w-6 h-6"
              />
            </TouchableOpacity>
        </View>
    </SafeAreaView>
  )
}

export default Profile
