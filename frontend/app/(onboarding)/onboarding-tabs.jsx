import { useState, useRef } from "react";
import { Link, router } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { View, Text, ScrollView, Dimensions, Image, StyleSheet, Alert } from "react-native";
import LottieView from 'lottie-react-native';

import { images } from '../../constants';
import Onboarding from 'react-native-onboarding-swiper';
import FormField from '../../components/FormField';
import CustomButton from "../../components/CustomButton";
import { onboarding } from "../../lib/appwrite";

import { useGlobalContext } from "../../context/GlobalProvider";

const { width, height } = Dimensions.get("window");

const OnboardingTabs = () => {

  const { user, setUser, setIsLogged } = useGlobalContext();

  const onboardingRef = useRef(null);

  const [outlook, setOutlook] = useState("");
  const [openAIAPI, setOpenAIAPI] = useState("");
  const [geminiAPI, setGeminiAPI] = useState("");
  const [slack, setSlack] = useState({
    slackID: "",
    slackEmail: "",
  });

  const handleAPIKeysContinue = async () => {
    if (openAIAPI === "" && geminiAPI === "") {
      Alert.alert("Error", "Please enter atleast one API key to continue");
    }
    if (slack.slackID === "" || slack.slackEmail === "") {
      Alert.alert("Error", "Please enter both Slack ID and Email to continue");
    }
    else {

      const onboardingData = {
        username : user.username,
        email: user.email,
        password : user.password,
        gemini_api_key: geminiAPI,
        openai_api_key: openAIAPI,
        slack_email : slack.slackEmail,
        slack_id : slack.slackID
      }

      const response = await onboarding(onboardingData);
      console.log(response);

      router.replace("/home");
    }
  }

  const handleSlackContinue = () => {
    if (slack.slackID === "" || slack.slackEmail === "") {
      Alert.alert("Error", "Please enter both Slack ID and Email to continue");
    }
    else {
        onboardingRef.current.goNext();
    }
  }


  return (
    // <SafeAreaView>
        <View style={styles.container}>
            <Onboarding
                ref={onboardingRef}
                bottomBarColor="#f5f3f0"
                controlStatusBar={false}
                skipLabel=""
                nextLabel=""
                pages={[
                    // {
                    //   backgroundColor: '#f5f3f0',
                    //   image: (
                    //     <View style={styles.lottie}>
                    //         <LottieView style={{flex: 1}} source={require('../../assets/animations/mail.json')}  autoPlay loop={false}/>
                    //         <View className="flex items-center">
                    //             <Text className="text-2xl font-pmedium mt-1">Enter Outlook Email</Text>
                    //         </View>
                    //         <View className="flex items-center">
                    //             <FormField
                    //                 placeholder=""
                    //                 value={outlook}
                    //                 onChangeText={setOutlook}
                    //             />
                    //         </View>
                    //         <View className="w-full mt-6 h-8">
                    //             <CustomButton 
                    //             title="Continue"
                    //             otherStyles="mt-6"
                    //             handlePress={handleContinueOutlook}
                    //             />
                    //         </View>
                    //     </View>
                    //   ),
                    //   title: (
                    //     <View className="flex items-center">
                            
                    //     </View>
                    //   ),
                    //   subtitle: '',
                    // },
                    {
                      backgroundColor: '#f5f3f0',
                      image: (
                        <View style={styles.lottie}>
                            <LottieView style={{flex: 1}} source={require('../../assets/animations/slack.json')}  autoPlay loop={false}/>
                            <View className="flex items-center">
                                <Text className="text-2xl font-pmedium">Enter Slack Credentials</Text>
                            </View>
                            <View className="flex items-center">
                                <FormField
                                    placeholder="Slack ID"
                                    value={slack.slackID}
                                    onChangeText={(e) => setSlack({ ...slack, slackID: e })}
                                />
                            </View>
                            <View className="flex items-center">
                                <FormField
                                    placeholder="Slack Email"
                                    value={slack.slackEmail}
                                  onChangeText={(e) => setSlack({ ...slack, slackEmail: e })}
                                />
                            </View>
                            <View className="w-full mt-6 h-1">
                                <CustomButton 
                                title="Continue"
                                otherStyles="mt-6"
                                handlePress={handleSlackContinue}
                                />
                            </View>
                        </View>
                      ),
                      title: (
                        <View className="flex items-center">
                            
                        </View>
                      ),
                      subtitle: '',
                    },
                    {
                        backgroundColor: '#f5f3f0',
                        image: (
                          <View style={styles.lottie}>
                              <LottieView style={{flex: 1}} source={require('../../assets/animations/api.json')}  autoPlay loop={true}/>
                              <View className="flex items-center">
                                  <Text className="text-2xl font-pmedium">Enter API Keys</Text>
                              </View>
                              <View className="flex items-center">
                                  <FormField
                                      placeholder="OpenAI API"
                                      value={openAIAPI}
                                      onChangeText={setOpenAIAPI}
                                  />
                              </View>
                              <View className="flex items-center">
                                  <FormField
                                      placeholder="Gemini API"
                                      value={geminiAPI}
                                      onChangeText={setGeminiAPI}
                                  />
                              </View>
                              <View className="w-full mt-6 h-1">
                                  <CustomButton 
                                  title="Continue"
                                  otherStyles="mt-6"
                                  handlePress={handleAPIKeysContinue}
                                  />
                              </View>
                          </View>
                        ),
                        title: (
                          <View className="flex items-center">
                              
                          </View>
                        ),
                        subtitle: '',
                      },
                  ]}
                  
            />
        </View>
    // </SafeAreaView>
        
  )
}

const styles = StyleSheet.create({
    container : {
        flex: 1,
        backgroundColor: 'white',
    },
    lottie : {
        width: width*0.9,
        height: width,
    }
});

export default OnboardingTabs