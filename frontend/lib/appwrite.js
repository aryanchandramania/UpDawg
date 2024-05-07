import {
    Account,
    Avatars,
    Client,
    Databases,
    ID,
    Query,
    Storage,
  } from "react-native-appwrite";


export const config = {
    endpoint: 'https://cloud.appwrite.io/v1',
    platform: 'com.jsm.updawg',
    projectId: '6627930826675a05ee8b',
    databaseId: '6627992cc8282009ebad',
    userCollectionId: '6627995f3cefae42f7cc',
}

// Init your react-native SDK
const client = new Client();

client
    .setEndpoint(config.endpoint) // Your Appwrite Endpoint
    .setProject(config.projectId) // Your project ID
    .setPlatform(config.platform) // Your application ID or bundle ID.
;

const account = new Account(client);
const databases = new Databases(client);

export async function createUser(email, password, username) {
    try {
      const newAccount = await account.create(
        ID.unique(),
        email,
        password,
        username
      );
  
      if (!newAccount) throw Error;
  
      await signIn(email, password);
  
      const newUser = await databases.createDocument(
        config.databaseId,
        config.userCollectionId,
        ID.unique(),
        {
          accountID: newAccount.$id,
          email: email,
          username: username,
        }
      );
  
      return newUser;
    } catch (error) {
      throw new Error(error);
    }
  }

  export async function signIn(email, password) {
    try {
      const session = await account.createEmailSession(email, password);
  
      return session;
    } catch (error) {
      throw new Error(error);
    }
  }

  export async function getAccount() {
    try {
      const currentAccount = await account.get();
  
      return currentAccount;
    } catch (error) {
      throw new Error(error);
    }
  }
  
  // Get Current User
  export async function getCurrentUser() {
    try {
      const currentAccount = await getAccount();
      if (!currentAccount) throw Error;
  
      const currentUser = await databases.listDocuments(
        config.databaseId,
        config.userCollectionId,
        [Query.equal("accountID", currentAccount.$id)]
      );
  
      if (!currentUser) throw Error;
  
      return currentUser.documents[0];
    } catch (error) {
      console.log(error);
      return null;
    }
  }

  export async function signOut() {
    try {
      const session = await account.deleteSession("current");
  
      return session;
    } catch (error) {
      throw new Error(error);
    }
  }

  export async function sendLoginData(loginData) {
    try {
      await fetch("http://192.168.2.224:3000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(loginData),
      })
        .then((res) => res.json())
        .then((data) => {
          console.log(data.message);
        });
    }
    catch (error) {
      throw new Error(error);
    }
  }

  export async function sendLogout() {
    try {
      await fetch("http://192.168.2.224:3000/logout", {
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          console.log(data.message);
        });

      }
      catch (error) {
        throw new Error(error);
      }
  }

  export async function sendSelection(days) {
    try {
      await fetch("http://192.168.2.224:3000/processRequest", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({"days": days}),
      })
        .then((res) => res.json())
        .then((data) => {
          console.log(data.message);
          return data.message;
        });
    }
    catch (error) {
      throw new Error(error);
    }
  }

  export async function onboarding(onboardingData) {
    try {
      await fetch("http://192.168.2.224:3000/onboarding", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(onboardingData),
      })
        .then((res) => res.json())
        .then((data) => {
          console.log(data.message);
        });
    }
    catch (error) {
      throw new Error(error);
    }
  }


//   export async function getHello() {
//     try {
//         const response = await fetch("http://192.168.2.224:3000/sendHello", {
//             method: "GET",
//         });
//         const data = await response.json();
//         console.log(data);
//         return data; // Optionally return data to the caller
//     } catch (error) {
//         console.error('Error fetching data:', error);
//         throw error;
//     }
// }

