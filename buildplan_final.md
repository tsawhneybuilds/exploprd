# **Step-by-Step Build Plan: Chat-PRD Page for Explo.co (Advanced)**

This guide provides a detailed, step-by-step plan to build your "Chat-PRD" page on the explo.co website. It focuses on the sequential actions you'll take, covering frontend development, Firebase backend services, and advanced AI integration, including robust document processing, dedicated vector database integration, conversation memory, and structured PRD export.

## **Goal**

Create a web page where product managers can:

* Upload PDF or Word documents.  
* Engage in a conversational AI chat that understands and responds based on the content of the uploaded documents and remembers previous interactions.  
* Generate and export structured PRD content (not just raw chat history) as a Word file.  
* The design will align with explo.co's aesthetic, utilizing DM Sans text and your established color scheme.

## **Phase 1: Foundation \- Firebase Project Setup & Local Environment**

This phase gets your Firebase project ready and your local machine set up to interact with it.

### **Step 1.1: Create Your Firebase Project**

This will be the central hub for all your Firebase services in the cloud.

1. **Go to Firebase Console:** Open your web browser and navigate to [https://console.firebase.google.com/](https://console.firebase.google.com/).  
2. **Sign In:** Sign in with your Google account.  
3. **Add Project:** Click on the "Add project" button.  
4. **Enter Project Name:** Give your project a descriptive name (e.g., "Explo Chat PRD"). Firebase will automatically generate a unique **Project ID** (e.g., explo-chat-prd-12345). Make a note of this ID; you'll use it often.  
5. **Google Analytics (Optional):** Decide if you want to enable Google Analytics. You can usually leave this enabled.  
6. **Create Project:** Click "Create project" and wait for it to be provisioned.  
7. **Continue:** Click "Continue" to go to your project's dashboard.

### **Step 1.2: Install and Log In to the Firebase CLI**

The Firebase Command Line Interface (CLI) is how you'll manage your Firebase project from your computer.

1. **Prerequisite: Node.js and npm:** If you don't have Node.js and npm (Node Package Manager) installed, download them from [https://nodejs.org/](https://nodejs.org/).  
2. **Install Firebase CLI:** Open your terminal or command prompt and run:  
   npm install \-g firebase-tools

3. **Log In to Firebase:** In your terminal, run:  
   firebase login

   * This will open a browser window for Google authentication. Log in with the same account you used for your Firebase project.

### **Step 1.3: Initialize Your Firebase Project Locally**

This connects your local development folder to your new Firebase project.

1. **Create Project Directory:** Create an empty folder for your app (e.g., my-chat-prd-app).  
   mkdir my-chat-prd-app  
   cd my-chat-prd-app

2. **Initialize Firebase:** Inside this new folder, run:  
   firebase init

3. **Follow the Prompts Carefully:**  
   * **"Are you ready to proceed? (Y/n)"**: Type Y.  
   * **"Which Firebase features do you want to set up...?"**: Use the **spacebar** to select **Firestore**, **Functions**, **Hosting**, and **Storage**. Then press Enter.  
   * **"Please select a default Firebase project..."**: Choose the project you created in Step 1.1 from the list.  
   * **Firestore Setup:** Accept defaults for rules (firestore.rules) and indexes (firestore.indexes.json).  
   * **Functions Setup:**  
     * **"What language would you like to use for Cloud Functions?"**: Choose Python.  
     * **"Do you want to install dependencies with pip?"**: Type Y.  
     * **"Do you want to use pipenv...?"**: Type N (unless you know you need pipenv).  
     * Accept default for Functions config (functions/main.py).  
   * **Hosting Setup:**  
     * **"What do you want to use as your public directory?"**: Type public and press Enter. This is where your website's files will go.  
     * **"Configure as a single-page app (rewrite all urls to /index.html)?"**: Type Y.  
   * **Storage Setup:** Accept default for Storage Rules (storage.rules).

The CLI will create public/, functions/, and configuration files like firestore.rules, storage.rules, firebase.json.

## **Phase 2: Frontend Development \- Building the User Interface**

This phase focuses on creating the web page that your users will interact with, including improved status feedback and document management.

### **Step 2.1: Create Core HTML Structure & Styling**

You'll set up the basic layout of your page, including styling consistent with explo.co.

1. **Create public/index.html:** Inside the public/ folder created by firebase init, create a new file named index.html.  
2. **Paste the following HTML content:** This includes the overall structure, Tailwind CSS CDN, and custom styles for explo.co's color scheme and font.  
   \<\!DOCTYPE html\>  
   \<html lang="en"\>  
   \<head\>  
       \<meta charset="UTF-8"\>  
       \<meta name="viewport" content="width=device-width, initial-scale=1.0"\>  
       \<title\>Chat-PRD | Explo\</title\>  
       \<\!-- Tailwind CSS CDN \--\>  
       \<script src="https://cdn.tailwindcss.com"\>\</script\>  
       \<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700\&display=swap" rel="stylesheet"\>  
       \<style\>  
           body {  
               font-family: 'DM Sans', sans-serif;  
               background-color: \#F5F5F5; /\* Light Grey from Explo.co \*/  
               color: \#333333; /\* Dark text color \*/  
           }  
           /\* Custom Tailwind colors matching Explo.co \*/  
           .bg-explo-blue { background-color: \#0000FF; } /\* Explo Blue \*/  
           .bg-explo-darkblue { background-color: \#000080; } /\* Dark Blue/Navy \*/  
           .text-explo-blue { color: \#0000FF; }  
           .border-explo-blue { border-color: \#0000FF; }  
           .ring-explo-blue { \--tw-ring-color: \#0000FF; }

           /\* Simple spinner for loading states \*/  
           .spinner {  
               border: 4px solid rgba(0, 0, 0, 0.1);  
               border-left-color: \#0000FF; /\* Explo Blue \*/  
               border-radius: 50%;  
               width: 16px;  
               height: 16px;  
               animation: spin 1s linear infinite;  
               display: inline-block;  
               vertical-align: middle;  
               margin-left: 8px;  
           }  
           @keyframes spin {  
               0% { transform: rotate(0deg); }  
               100% { transform: rotate(360deg); }  
           }  
       \</style\>  
   \</head\>  
   \<body class="min-h-screen flex flex-col"\>  
       \<\!-- Header (Mimicking Explo.co's header style) \--\>  
       \<header class="bg-white shadow-md p-4"\>  
           \<nav class="container mx-auto flex justify-between items-center"\>  
               \<div class="text-2xl font-bold text-explo-blue"\>  
                   \<a href="https://www.explo.co/" class="hover:underline"\>Explo.co\</a\>  
               \</div\>  
               \<div class="space-x-4"\>  
                   \<a href="\#" class="text-gray-700 hover:text-explo-blue font-medium"\>Chat-PRD\</a\>  
                   \<\!-- Placeholder for User ID display \--\>  
                   \<span id="userIdDisplay" class="ml-4 text-xs text-gray-500"\>\</span\>  
               \</div\>  
           \</nav\>  
       \</header\>

       \<\!-- Main Content Area \--\>  
       \<main class="flex-grow container mx-auto p-4 md:p-8 flex flex-col lg:flex-row gap-8"\>  
           \<\!-- Document Upload & Info Area \--\>  
           \<div class="lg:w-1/3 bg-white p-6 rounded-lg shadow-md flex flex-col space-y-4"\>  
               \<h2 class="text-xl font-bold"\>Document Management\</h2\>  
               \<p class="text-gray-600"\>Upload your PDF or Word document to start building your PRD.\</p\>  
               \<input type="file" id="documentUpload" accept=".pdf,.doc,.docx" class="block w-full text-sm text-gray-500  
                                                       file:mr-4 file:py-2 file:px-4  
                                                       file:rounded-full file:border-0  
                                                       file:text-sm file:font-semibold  
                                                       file:bg-explo-blue file:text-white  
                                                       hover:file:bg-explo-darkblue cursor-pointer"\>  
               \<div id="uploadStatus" class="text-sm text-gray-600"\>\</div\>

               \<h3 class="text-lg font-bold mt-4"\>Uploaded Documents\</h3\>  
               \<ul id="uploadedDocumentsList" class="space-y-2 text-gray-700"\>  
                   \<\!-- Dynamically loaded documents will go here \--\>  
                   \<li class="text-gray-500 text-sm"\>No documents uploaded yet.\</li\>  
               \</ul\>

               \<button id="exportPrdBtn" class="mt-auto px-4 py-2 bg-green-500 text-white font-semibold rounded-full shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75 disabled:opacity-50"\>  
                   Export Generated PRD  
                   \<span id="exportSpinner" class="spinner hidden"\>\</span\>  
               \</button\>  
           \</div\>

           \<\!-- Chat Area \--\>  
           \<div class="lg:w-2/3 bg-white p-6 rounded-lg shadow-md flex flex-col"\>  
               \<h2 class="text-xl font-bold mb-4"\>Chat with your PRD\</h2\>  
               \<div id="chatWindow" class="flex-grow overflow-y-auto border border-gray-200 rounded-lg p-4 mb-4 space-y-4 bg-gray-50"\>  
                   \<\!-- Chat messages will be appended here \--\>  
                   \<div class="flex items-start"\>  
                       \<div class="flex-shrink-0 w-8 h-8 rounded-full bg-explo-blue flex items-center justify-center text-white text-sm font-bold mr-3"\>AI\</div\>  
                       \<div class="bg-gray-200 p-3 rounded-xl max-w-\[80%\]"\>  
                           \<p class="text-sm text-gray-800"\>Hello\! Upload a document to start building your PRD. I'm ready to assist you.\</p\>  
                       \</div\>  
                   \</div\>  
               \</div\>

               \<div class="flex items-center space-x-3"\>  
                   \<input type="text" id="chatInput" placeholder="Ask a question or provide a prompt..." class="flex-grow p-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-explo-blue"\>  
                   \<button id="sendChatBtn" clacss="px-5 py-3 bg-explo-blue text-white font-semibold rounded-full shadow-md hover:bg-explo-darkblue focus:outline-none focus:ring-2 focus:ring-explo-blue focus:ring-opacity-75"\>  
                       Send  
                       \<span id="chatSpinner" class="spinner hidden"\>\</span\>  
                   \</button\>  
               \</div\>  
               \<div id="chatStatus" class="text-sm text-gray-600 mt-2"\>\</div\>  
           \</div\>  
       \</main\>

       \<\!-- Footer (Basic, can be expanded) \--\>  
       \<footer class="bg-explo-darkblue text-white p-4 text-center mt-8"\>  
           \<p\>© 2025 Explo. All rights reserved.\</p\>  
       \</footer\>

       \<\!-- Firebase SDKs & App Logic \- will be added here \--\>  
   \</body\>  
   \</html\>

### **Step 2.2: Add Frontend JavaScript Logic**

You'll add the client-side JavaScript that interacts with your Firebase services. This goes at the end of the body tag in public/index.html.

1. **Add script tag:** Below the footer, add the main \<script type="module"\> block.  
2. **Paste the following JavaScript:** This includes Firebase SDK imports, initialization, UI helpers, and event listeners for upload, chat, and export.  
   * **Crucially, remember to replace YOUR\_CLOUD\_FUNCTION\_REGION and YOUR\_PROJECT\_ID placeholders with your actual values from Step 1.1 and your Cloud Functions deployment.**

\<script type="module"\>  
    // Firebase imports  
    import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";  
    import { getAuth, signInAnonymously, onAuthStateChanged, signInWithCustomToken } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";  
    import { getStorage, ref as storageRef, uploadBytes, getDownloadURL, deleteObject } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-storage.js";  
    import { getFirestore, doc, collection, addDoc, onSnapshot, query, orderBy, serverTimestamp, getDocs, updateDoc, deleteDoc } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

    // Firebase Configuration (THIS WILL BE PROVIDED BY THE CANVAS ENVIRONMENT)  
    const appId \= typeof \_\_app\_id \!== 'undefined' ? \_\_app\_id : 'default-app-id';  
    const firebaseConfig \= typeof \_\_firebase\_config \!== 'undefined' ? JSON.parse(\_\_firebase\_config) : {};

    // Initialize Firebase variables  
    let app;  
    let db;  
    let auth;  
    let storage;  
    let userId;

    // Get UI elements  
    const chatWindow \= document.getElementById('chatWindow');  
    const chatInput \= document.getElementById('chatInput');  
    const sendChatBtn \= document.getElementById('sendChatBtn');  
    const documentUpload \= document.getElementById('documentUpload');  
    const uploadStatus \= document.getElementById('uploadStatus');  
    const uploadedDocumentsList \= document.getElementById('uploadedDocumentsList');  
    const exportPrdBtn \= document.getElementById('exportPrdBtn');  
    const chatStatus \= document.getElementById('chatStatus');  
    const userIdDisplay \= document.getElementById('userIdDisplay');  
    const chatSpinner \= document.getElementById('chatSpinner');  
    const exportSpinner \= document.getElementById('exportSpinner');

    let isAuthReady \= false;  
    let processedDocuments \= {}; // Stores {docId: {name, status, extractedText}}

    // \--- Firebase Initialization and Authentication \---  
    async function initFirebase() {  
        try {  
            app \= initializeApp(firebaseConfig);  
            db \= getFirestore(app);  
            auth \= getAuth(app);  
            storage \= getStorage(app);

            if (typeof \_\_initial\_auth\_token \!== 'undefined') {  
                await signInWithCustomToken(auth, \_\_initial\_auth\_token);  
            } else {  
                await signInAnonymously(auth);  
            }

            onAuthStateChanged(auth, (user) \=\> {  
                if (user) {  
                    userId \= user.uid;  
                    console.log("Firebase User ID:", userId);  
                    isAuthReady \= true;  
                    userIdDisplay.textContent \= \`User: ${userId}\`;  
                    setupRealtimeListeners();  
                    exportPrdBtn.disabled \= false;  
                } else {  
                    console.log("No user signed in.");  
                    userId \= null;  
                    userIdDisplay.textContent \= 'User: Not authenticated';  
                    exportPrdBtn.disabled \= true;  
                }  
            });  
        } catch (error) {  
            console.error("Error initializing Firebase:", error);  
            showStatus(uploadStatus, \`Error initializing app: ${error.message}\`, 'error');  
        }  
    }

    // \--- Realtime Listeners for Documents and Chat \---  
    function setupRealtimeListeners() {  
        if (\!isAuthReady) {  
            console.warn("Authentication not ready for listeners.");  
            return;  
        }

        // Listen for uploaded documents  
        const docsCollectionRef \= collection(db, \`artifacts/${appId}/users/${userId}/documents\`);  
        onSnapshot(docsCollectionRef, (snapshot) \=\> {  
            uploadedDocumentsList.innerHTML \= '';  
            if (snapshot.empty) {  
                uploadedDocumentsList.innerHTML \= '\<li class="text-gray-500 text-sm"\>No documents uploaded yet.\</li\>';  
            } else {  
                snapshot.forEach((doc) \=\> {  
                    const data \= doc.data();  
                    const docId \= doc.id;  
                    processedDocuments\[docId\] \= data; // Store document data locally

                    const listItem \= document.createElement('li');  
                    listItem.className \= 'p-2 bg-gray-100 rounded-md flex justify-between items-center';  
                    listItem.innerHTML \= \`  
                        \<span class="truncate"\>${data.name}\</span\>  
                        \<div class="flex items-center space-x-2"\>  
                            \<span class="text-xs ${data.status \=== 'Processed' ? 'text-green-600' : 'text-yellow-600'}"\>${data.status}\</span\>  
                            \<button class="text-red-500 hover:text-red-700 text-sm font-bold delete-doc-btn" data-doc-id="${docId}" data-storage-path="${data.storagePath}"\>  
                                \<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"\>  
                                    \<path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 011-1h4a1 1 0 110 2H8a1 1 0 01-1-1zm6 0a1 1 0 011-1h1a1 1 0 110 2h-1a1 1 0 01-1-1zm-3 4a1 1 0 011-1h1a1 1 0 110 2h-1a1 1 0 01-1-1z" clip-rule="evenodd" /\>  
                                \</svg\>  
                            \</button\>  
                        \</div\>  
                    \`;  
                    uploadedDocumentsList.appendChild(listItem);  
                });  
                 // Attach event listeners to new delete buttons  
                document.querySelectorAll('.delete-doc-btn').forEach(button \=\> {  
                    button.addEventListener('click', handleDeleteDocument);  
                });  
            }  
        }, (error) \=\> {  
            console.error("Error fetching documents:", error);  
            showStatus(uploadStatus, \`Error loading documents: ${error.message}\`, 'error');  
        });

        // Listen for chat messages  
        const chatCollectionRef \= collection(db, \`artifacts/${appId}/users/${userId}/chatHistory\`);  
        const q \= query(chatCollectionRef, orderBy('timestamp'));

        onSnapshot(q, (snapshot) \=\> {  
            chatWindow.innerHTML \= '';  
            snapshot.forEach((doc) \=\> {  
                const message \= doc.data();  
                displayMessage(message.text, message.role \=== 'user');  
            });  
            chatWindow.scrollTop \= chatWindow.scrollHeight;  
        }, (error) \=\> {  
            console.error("Error fetching chat history:", error);  
            showStatus(chatStatus, \`Error loading chat: ${error.message}\`, 'error');  
        });  
    }

    // \--- UI Helper Functions \---  
    function displayMessage(text, isUser) {  
        const messageContainer \= document.createElement('div');  
        messageContainer.className \= \`flex items-start ${isUser ? 'justify-end' : ''}\`;

        // Basic Markdown to HTML conversion for AI responses  
        let formattedText \= text;  
        if (\!isUser) {  
             formattedText \= formattedText  
                .replace(/\\\*\\\*(.\*?)\\\*\\\*/g, '\<strong\>$1\</strong\>') // Bold  
                .replace(/\\\*(.\*?)\\\*/g, '\<em\>$1\</em\>') // Italic  
                .replace(/^- (.\*)/gm, '\<li\>$1\</li\>') // List items  
                .replace(/\`(\[^\`\]+)\`/g, '\<code\>$1\</code\>'); // Inline code  
             if (formattedText.includes('\<li\>')) {  
                 formattedText \= \`\<ul\>${formattedText}\</ul\>\`;  
             }  
        }

        const avatar \= document.createElement('div');  
        avatar.className \= \`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold mr-3 ${isUser ? 'hidden' : 'bg-explo-blue'}\`;  
        avatar.textContent \= isUser ? '' : 'AI';

        const userAvatar \= document.createElement('div');  
        userAvatar.className \= \`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold ml-3 ${isUser ? 'bg-gray-500' : 'hidden'}\`;  
        userAvatar.textContent \= isUser ? 'You' : '';

        const messageBubble \= document.createElement('div');  
        messageBubble.className \= \`p-3 rounded-xl max-w-\[80%\] ${isUser ? 'bg-explo-blue text-white' : 'bg-gray-200 text-gray-800'}\`;  
        messageBubble.innerHTML \= \`\<p class="text-sm"\>${formattedText}\</p\>\`;

        if (isUser) {  
            messageContainer.appendChild(messageBubble);  
            messageContainer.appendChild(userAvatar);  
        } else {  
            messageContainer.appendChild(avatar);  
            messageContainer.appendChild(messageBubble);  
        }  
        chatWindow.appendChild(messageContainer);  
    }

    function showStatus(element, message, type \= 'info', isLoading \= false) {  
        element.innerHTML \= message; // Use innerHTML to allow spinner element  
        element.className \= \`text-sm mt-2 ${type \=== 'error' ? 'text-red-600' : type \=== 'success' ? 'text-green-600' : 'text-gray-600'}\`;  
        const spinner \= element.nextElementSibling; // Assuming spinner is next sibling  
        if (spinner && spinner.classList.contains('spinner')) {  
            if (isLoading) {  
                spinner.classList.remove('hidden');  
            } else {  
                spinner.classList.add('hidden');  
            }  
        }  
    }

    // \--- Event Listeners \---

    // Document Upload  
    documentUpload.addEventListener('change', async (event) \=\> {  
        const file \= event.target.files\[0\];  
        if (\!file) {  
            showStatus(uploadStatus, 'No file selected.', 'info');  
            return;  
        }

        if (\!userId) {  
            showStatus(uploadStatus, 'Please wait, authenticating...', 'error');  
            return;  
        }

        showStatus(uploadStatus, \`Uploading ${file.name}...\<span class="spinner"\>\</span\>\`, 'info', true);  
        sendChatBtn.disabled \= true; // Disable chat during upload/processing  
        exportPrdBtn.disabled \= true;

        const fileExtension \= file.name.split('.').pop().toLowerCase();  
        if (\!\['pdf', 'doc', 'docx'\].includes(fileExtension)) {  
            showStatus(uploadStatus, 'Unsupported file type. Please upload a PDF or Word document.', 'error', false);  
            sendChatBtn.disabled \= false;  
            exportPrdBtn.disabled \= false;  
            return;  
        }

        try {  
            // 1\. Upload file to Cloud Storage  
            const fileRef \= storageRef(storage, \`artifacts/${appId}/users/${userId}/uploads/${file.name}\`);  
            const snapshot \= await uploadBytes(fileRef, file);  
            const downloadURL \= await getDownloadURL(snapshot.ref);

            showStatus(uploadStatus, \`File uploaded to storage. Processing...\<span class="spinner"\>\</span\>\`, 'info', true);

            // 2\. Store document metadata in Firestore (this will trigger Cloud Function)  
            const docRef \= await addDoc(collection(db, \`artifacts/${appId}/users/${userId}/documents\`), {  
                name: file.name,  
                storagePath: snapshot.ref.fullPath,  
                downloadURL: downloadURL,  
                uploadedAt: serverTimestamp(),  
                status: 'Uploaded', // Initial status  
                userId: userId  
            });

            showStatus(uploadStatus, \`Document '${file.name}' submitted for processing. Status will update.\`, 'success', false);

            // The actual processing will happen in a Cloud Function triggered by the Firestore write or Storage upload.  
            // The status will then update via the Firestore listener (setupRealtimeListeners)  
            await updateDoc(doc(db, \`artifacts/${appId}/users/${userId}/documents\`, docRef.id), { status: 'Processing...' }); // Optimistic update

        } catch (error) {  
            console.error("Error uploading or processing document:", error);  
            showStatus(uploadStatus, \`Error uploading/processing: ${error.message}\`, 'error', false);  
        } finally {  
            sendChatBtn.disabled \= false;  
            exportPrdBtn.disabled \= false;  
        }  
    });

    // Handle Delete Document  
    async function handleDeleteDocument(event) {  
        const button \= event.currentTarget;  
        const docId \= button.dataset.docId;  
        const storagePath \= button.dataset.storagePath;

        if (\!confirm(\`Are you sure you want to delete '${button.closest('li').querySelector('span.truncate').textContent}'? This action cannot be undone.\`)) {  
            return;  
        }

        showStatus(uploadStatus, \`Deleting document...\<span class="spinner"\>\</span\>\`, 'info', true);  
        button.disabled \= true; // Disable the specific button

        try {  
            // 1\. Delete from Cloud Storage  
            const fileRef \= storageRef(storage, storagePath);  
            await deleteObject(fileRef);  
            console.log("File deleted from storage:", storagePath);

            // 2\. Delete from Firestore  
            await deleteDoc(doc(db, \`artifacts/${appId}/users/${userId}/documents\`, docId));  
            console.log("Document metadata deleted from Firestore:", docId);

            // Remove from local cache  
            delete processedDocuments\[docId\];

            showStatus(uploadStatus, 'Document deleted successfully.', 'success', false);  
        } catch (error) {  
            console.error("Error deleting document:", error);  
            showStatus(uploadStatus, \`Error deleting document: ${error.message}\`, 'error', false);  
        } finally {  
            button.disabled \= false; // Re-enable if deletion failed  
        }  
    }

    // Send Chat Message  
    chatInput.addEventListener('keypress', (event) \=\> {  
        if (event.key \=== 'Enter') {  
            sendChatBtn.click(); // Trigger button click on Enter key  
        }  
    });

    sendChatBtn.addEventListener('click', async () \=\> {  
        const messageText \= chatInput.value.trim();  
        if (\!messageText) return;

        if (\!userId) {  
            showStatus(chatStatus, 'Please wait, authenticating...', 'error');  
            return;  
        }

        displayMessage(messageText, true);  
        chatInput.value \= '';  
        sendChatBtn.disabled \= true;  
        chatSpinner.classList.remove('hidden'); // Show spinner  
        showStatus(chatStatus, 'Thinking...\<span class="spinner"\>\</span\>', 'info', true);

        // Save user message to Firestore  
        await addDoc(collection(db, \`artifacts/${appId}/users/${userId}/chatHistory\`), {  
            role: 'user',  
            text: messageText,  
            timestamp: serverTimestamp(),  
            userId: userId  
        });

        try {  
            // IMPORTANT: In a robust RAG setup, document context and chat history  
            // are primarily fetched and processed on the backend (Cloud Function)  
            // for security, efficiency, and to avoid large payloads from frontend.  
            // The frontend sending \`documentContext\` is a simplified placeholder.  
            // The backend \`chatWithDocument\` function will perform proper RAG.

            const payload \= {  
                message: messageText,  
                userId: userId,  
                // documentContext is no longer needed from frontend if backend does RAG properly  
            };

            const response \= await fetch(\`https://YOUR\_CLOUD\_FUNCTION\_REGION-YOUR\_PROJECT\_ID.cloudfunctions.net/chatWithDocument\`, {  
                method: 'POST',  
                headers: { 'Content-Type': 'application/json' },  
                body: JSON.stringify(payload)  
            });

            const result \= await response.json();

            if (response.ok && result.response) {  
                await addDoc(collection(db, \`artifacts/${appId}/users/${userId}/chatHistory\`), {  
                    role: 'ai',  
                    text: result.response,  
                    timestamp: serverTimestamp(),  
                    userId: userId  
                });  
                showStatus(chatStatus, 'Response received.', 'success', false);  
            } else {  
                console.error("Error from chatbot function:", result.error || response.statusText);  
                showStatus(chatStatus, \`Error: ${result.error || 'Failed to get response.'}\`, 'error', false);  
                displayMessage("Sorry, I encountered an error. Please try again.", false);  
            }  
        } catch (error) {  
            console.error("Error sending chat message:", error);  
            showStatus(chatStatus, \`Error: ${error.message}\`, 'error', false);  
            displayMessage("Sorry, something went wrong. Please check your connection or try again later.", false);  
        } finally {  
            sendChatBtn.disabled \= false;  
            chatSpinner.classList.add('hidden'); // Hide spinner  
        }  
    });

    // Export PRD as Word  
    exportPrdBtn.addEventListener('click', async () \=\> {  
        if (\!userId) {  
            showStatus(uploadStatus, 'Please log in to export.', 'error');  
            return;  
        }

        showStatus(uploadStatus, 'Preparing PRD for export...\<span class="spinner"\>\</span\>', 'info', true);  
        exportPrdBtn.disabled \= true;  
        sendChatBtn.disabled \= true; // Disable chat during export

        // In a real scenario, you might send a specific prompt to the AI  
        // to generate the PRD content, or provide criteria for content selection.  
        // For this updated plan, we'll tell the Cloud Function to generate it.  
        const payload \= {  
            userId: userId,  
            // Add any specific instructions for PRD generation if needed, e.g.:  
            // prdInstructions: "Summarize key features, user stories, and technical requirements based on uploaded documents and chat history."  
        };

        try {  
            const response \= await fetch(\`https://YOUR\_CLOUD\_FUNCTION\_REGION-YOUR\_PROJECT\_ID.cloudfunctions.net/exportPRD\`, {  
                method: 'POST',  
                headers: { 'Content-Type': 'application/json' },  
                body: JSON.stringify(payload)  
            });

            const result \= await response.json();

            if (response.ok && result.downloadURL) {  
                showStatus(uploadStatus, 'PRD ready for download\!', 'success', false);  
                const a \= document.createElement('a');  
                a.href \= result.downloadURL;  
                a.download \= \`Explo\_PRD\_${new Date().toISOString().slice(0, 10)}.docx\`;  
                document.body.appendChild(a);  
                a.click();  
                document.body.removeChild(a);  
            } else {  
                console.error("Error from export function:", result.error || response.statusText);  
                showStatus(uploadStatus, \`Error exporting PRD: ${result.error || 'Failed to create file.'}\`, 'error', false);  
            }  
        } catch (error) {  
            console.error("Error exporting PRD:", error);  
            showStatus(uploadStatus, \`Error: ${error.message}\`, 'error', false);  
        } finally {  
            exportPrdBtn.disabled \= false;  
            sendChatBtn.disabled \= false;  
            exportSpinner.classList.add('hidden'); // Hide spinner  
        }  
    });

    // Initialize Firebase when the window loads  
    window.onload \= initFirebase;  
\</script\>

## **Phase 3: Firebase Security Rules \- Protecting Your Data**

Before you deploy anything, it's critical to set up rules that protect your user data in Firebase.

### **Step 3.1: Configure Firestore Security Rules**

1. **Open firestore.rules:** In your project's root directory, open the firestore.rules file that firebase init created.  
2. **Paste the following rules:** These rules ensure that each user can only read and write to their own data within the artifacts/{appId}/users/{userId}/ path.  
   rules\_version \= '2';  
   service cloud.firestore {  
     match /databases/{database}/documents {  
       // Private user data: Each user can only access their own data  
       match /artifacts/{appId}/users/{userId}/{collectionName} {  
         allow read, write: if request.auth \!= null && request.auth.uid \== userId;  
       }  
     }  
   }

### **Step 3.2: Configure Cloud Storage Security Rules**

1. **Open storage.rules:** In your project's root directory, open the storage.rules file.  
2. **Paste the following rules:** These rules similarly ensure users can only upload and download files to/from their designated personal folders in Cloud Storage.  
   rules\_version \= '2';  
   service firebase.storage {  
     match /b/{bucket}/o {  
       // Private user files: Each user can only access their own files  
       match /artifacts/{appId}/users/{userId}/{allPaths=\*\*} {  
         allow read, write: if request.auth \!= null && request.auth.uid \== userId;  
       }  
     }  
   }

## **Phase 4: Backend Development \- Cloud Functions for Logic & AI**

This is where the "brains" of your application reside. You'll write Python code that runs on Google's serverless infrastructure. This section now fully incorporates advanced RAG, robust parsing, and PRD generation.

### **Step 4.1: Prepare Cloud Functions Environment & Dependencies**

1. **Navigate to functions/:** Open your terminal and change into the functions/ directory inside your project.  
2. **Edit functions/requirements.txt:** This file lists all the Python libraries your Cloud Functions will need. Add the following.  
   * **Note on Flask:** While Cloud Functions can respond to HTTP requests directly, using a micro-framework like Flask can sometimes make handling request/response easier, especially for CORS (Cross-Origin Resource Sharing).

firebase-admin  
google-cloud-storage  
google-cloud-firestore  
google-cloud-aiplatform  
pypdf \# For PDF parsing  
python-docx \# For Word parsing and generation  
Flask \# For HTTP functions  
Flask-Cors \# For CORS handling with Flask  
scikit-learn \# For cosine similarity if implementing simple RAG without dedicated vector DB

### **Step 4.2: Global Imports and Initialization for Cloud Functions**

1. **Open functions/main.py:** This is where you'll write your Python Cloud Functions.  
2. **Add all necessary imports and global initializations:**  
   import os  
   import tempfile  
   from firebase\_admin import initialize\_app, firestore, storage  
   from firebase\_functions import storage\_fn, https\_fn  
   from google.cloud import storage as gcs\_client  
   from google.cloud import aiplatform  
   from pypdf import PdfReader  
   from docx import Document  
   import json  
   import logging  
   from flask import Request, jsonify \# Using Flask for HTTP functions for better structure  
   from flask\_cors import CORS \# For CORS handling  
   from sklearn.metrics.pairwise import cosine\_similarity \# For simple RAG similarity (if not using dedicated vector DB)  
   import numpy as np \# For numpy arrays

   \# Initialize Firebase Admin SDK  
   initialize\_app()  
   db \= firestore.client()  
   gcs \= gcs\_client.Client()

   \# Configure logging  
   logging.basicConfig(level=logging.INFO)

   \# Initialize Vertex AI for Gemini (replace with your project details)  
   \# Ensure aiplatform.init is called with your project\_id and location  
   \# Set these as environment variables in firebase.json (see Step 4.5)  
   PROJECT\_ID \= os.environ.get('GCP\_PROJECT', 'YOUR\_PROJECT\_ID') \# Will be set by Firebase env  
   REGION \= os.environ.get('FUNCTION\_REGION', 'us-central1') \# Will be set by Firebase env  
   aiplatform.init(project=PROJECT\_ID, location=REGION)

   \# Gemini Models  
   text\_model \= aiplatform.GenerativeModel(model\_name="gemini-1.5-flash") \# Use flash for speed  
   embedding\_model \= aiplatform.Preview.from\_pretrained('textembedding-gecko') \# For embeddings

   \# Create a Flask app for HTTP functions for consistent CORS handling  
   \# Note: For simple HTTP functions without complex routing, you can directly  
   \# use @https\_fn.on\_request. For multiple functions sharing a Flask context,  
   \# consider creating a \`flask.Flask\` instance if necessary. For clarity here,  
   \# each HTTP function will handle its own CORS with \`jsonify\` and \`headers\`.

   \# Define chunk size for RAG (adjust based on model token limits and document size)  
   RAG\_CHUNK\_SIZE \= 1000 \# characters  
   RAG\_CHUNK\_OVERLAP \= 200 \# characters

### **Step 4.3: Implement processDocument Cloud Function (with Advanced Parsing & Embedding Storage)**

This function will automatically process documents as they are uploaded. This is where robust parsing and embedding generation (for a vector database) happen.

1. **Add processDocument to functions/main.py:**  
   \# ... (Existing imports and initialization)

   @storage\_fn.on\_object\_finalized(bucket=f'{PROJECT\_ID}.appspot.com', region=REGION)  
   def processDocument(event: storage\_fn.StorageObjectData):  
       """  
       Cloud Function triggered when a new file is uploaded to Firebase Storage.  
       It extracts text, generates embeddings, and updates Firestore.  
       This version aims for more robust parsing and prepares for vector DB integration.  
       """  
       logging.info(f"Processing new file: {event.name}")

       if not event.name or event.name.endswith('/'): \# Skip directories  
           logging.info("Skipping directory or empty name event.")  
           return

       file\_bucket \= event.bucket  
       file\_name \= event.name  
       content\_type \= event.content\_type  
       \# Extract user\_id from the storage path: artifacts/{appId}/users/{userId}/uploads/file.name  
       try:  
           path\_parts \= file\_name.split('/')  
           app\_id\_from\_path \= path\_parts\[1\]  
           user\_id \= path\_parts\[3\]  
           if app\_id\_from\_path \!= PROJECT\_ID: \# Basic check for security  
               logging.error(f"App ID mismatch in path: {app\_id\_from\_path} vs {PROJECT\_ID}")  
               return  
       except IndexError:  
           logging.error(f"Could not parse user ID from path: {file\_name}")  
           return

       \# Ensure the file is in the 'uploads' path  
       if not 'uploads/' in file\_name:  
           logging.info(f"Skipping file not in uploads path: {file\_name}")  
           return

       extracted\_text \= ""  
       temp\_file\_path \= None  
       doc\_ref \= None \# Firestore document reference

       try:  
           \# 1\. Find the corresponding document entry in Firestore (added by frontend)  
           docs\_query \= db.collection(f'artifacts/{PROJECT\_ID}/users/{user\_id}/documents').where('storagePath', '==', file\_name)  
           docs \= docs\_query.get()  
           if not docs:  
               logging.warning(f"Firestore document for {file\_name} not found. Skipping processing.")  
               return  
           for doc\_found in docs:  
               doc\_ref \= db.collection(f'artifacts/{PROJECT\_ID}/users/{user\_id}/documents').document(doc\_found.id)  
               doc\_data \= doc\_found.to\_dict()  
               break \# Assuming one matching doc

           if not doc\_ref:  
               logging.error(f"Could not find Firestore doc reference for {file\_name}")  
               return

           doc\_ref.update({'status': 'Downloading and Parsing'})

           \# 2\. Download file from Cloud Storage  
           bucket \= storage.bucket(file\_bucket)  
           blob \= bucket.blob(file\_name)  
           temp\_file\_path \= os.path.join(tempfile.gettempdir(), os.path.basename(file\_name))  
           blob.download\_to\_filename(temp\_file\_path)  
           logging.info(f"File {file\_name} downloaded to {temp\_file\_path}")

           \# 3\. Extract text based on content type (more robust)  
           if content\_type \== 'application/pdf':  
               reader \= PdfReader(temp\_file\_path)  
               for page in reader.pages:  
                   page\_text \= page.extract\_text()  
                   if page\_text:  
                       extracted\_text \+= page\_text \+ "\\n"  
           elif content\_type in \['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'\]:  
               document \= Document(temp\_file\_path)  
               for paragraph in document.paragraphs:  
                   extracted\_text \+= paragraph.text \+ "\\n"  
           else:  
               logging.warning(f"Unsupported file type for text extraction: {content\_type}")  
               doc\_ref.update({'status': 'Failed: Unsupported Type'})  
               return

           if not extracted\_text.strip():  
               logging.warning(f"No text extracted from {file\_name}")  
               doc\_ref.update({'status': 'Failed: No Text Extracted'})  
               return

           doc\_ref.update({'status': 'Chunking and Embedding'})

           \# 4\. Text Chunking (with overlap for better context)  
           chunks \= \[\]  
           for i in range(0, len(extracted\_text), RAG\_CHUNK\_SIZE \- RAG\_CHUNK\_OVERLAP):  
               chunk \= extracted\_text\[i : i \+ RAG\_CHUNK\_SIZE\]  
               chunks.append(chunk)

           \# 5\. Generate Embeddings and Store in Firestore (for simple RAG) or prepare for Vector DB  
           \# For demonstration, we store embeddings and chunks in a subcollection of the document.  
           \# For large-scale RAG, a dedicated vector database is HIGHLY recommended for performance.  
           \# Firestore has a 1MB limit per document, so large extractedText should not be stored directly  
           \# in the parent document. Store in subcollection or dedicated service.

           batch \= db.batch()  
           chunks\_collection\_ref \= doc\_ref.collection('chunks') \# Subcollection for chunks  
           for i, chunk in enumerate(chunks):  
               if not chunk.strip(): continue \# Skip empty chunks  
               try:  
                   embedding\_response \= embedding\_model.predict(\[chunk\])  
                   embedding \= embedding\_response.embeddings\[0\].values  
                   chunk\_doc\_ref \= chunks\_collection\_ref.document(str(i)) \# Use index as ID  
                   batch.set(chunk\_doc\_ref, {  
                       'text': chunk,  
                       'embedding': embedding,  
                       'timestamp': firestore.SERVER\_TIMESTAMP  
                   })  
               except Exception as embed\_e:  
                   logging.error(f"Error generating embedding for chunk {i}: {embed\_e}")  
                   \# Decide if you want to fail the whole doc or just skip this chunk  
                   continue  
           batch.commit()  
           logging.info(f"Generated and stored {len(chunks)} chunks and embeddings for {file\_name}")

           \# Update master document status to Processed  
           doc\_ref.update({  
               'status': 'Processed',  
               \# 'extractedText': extracted\_text\[:900000\], \# ONLY IF \<= 1MB and you truly need it.  
                                                       \# Otherwise, rely on chunks subcollection.  
               'processedAt': firestore.SERVER\_TIMESTAMP,  
               'chunkCount': len(chunks)  
           })  
           logging.info(f"Document {file\_name} processing complete.")

       except Exception as e:  
           logging.error(f"Unhandled error processing document {file\_name}: {e}", exc\_info=True)  
           if doc\_ref:  
               doc\_ref.update({'status': f'Failed: {str(e)}'})  
       finally:  
           if temp\_file\_path and os.path.exists(temp\_file\_path):  
               os.remove(temp\_file\_path)  
               logging.info(f"Cleaned up temporary file: {temp\_file\_path}")

### **Step 4.4: Implement chatWithDocument Cloud Function (with Advanced RAG & Memory)**

This function will handle the AI conversation, now fully incorporating document context via RAG and remembering chat history.

1. **Add chatWithDocument to functions/main.py:**  
   \# ... (Existing imports and initialization)

   @https\_fn.on\_request(region=REGION)  
   def chatWithDocument(req: https\_fn.Request):  
       """  
       Cloud Function that processes chat messages, performs RAG on documents,  
       retrieves chat history for memory, and interacts with the Gemini API.  
       """  
       logging.info("Chat request received.")  
       \# Handle CORS preflight request  
       if req.method \== 'OPTIONS':  
           headers \= {  
               'Access-Control-Allow-Origin': '\*',  
               'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',  
               'Access-Control-Allow-Headers': 'Content-Type, Authorization',  
               'Access-Control-Max-Age': '3600'  
           }  
           return https\_fn.Response('', headers=headers, status=204)

       headers \= {  
           'Access-Control-Allow-Origin': '\*',  
           'Content-Type': 'application/json'  
       }

       try:  
           request\_json \= req.get\_json(silent=True)  
           if not request\_json:  
               return jsonify({"error": "Invalid JSON"}), 400, headers

           user\_message \= request\_json.get('message')  
           user\_id \= request\_json.get('userId')

           if not user\_message or not user\_id:  
               return jsonify({"error": "Missing message or userId"}), 400, headers

           logging.info(f"User {user\_id} message: {user\_message}")

           \# \--- 1\. Fetch Recent Chat History (for memory) \---  
           \# Fetch last 10 messages (user and AI)  
           chat\_history\_query \= db.collection(f'artifacts/{PROJECT\_ID}/users/{user\_id}/chatHistory').order\_by('timestamp', direction=firestore.Query.DESCENDING).limit(10)  
           chat\_history\_docs \= chat\_history\_query.get()

           formatted\_history \= \[\]  
           \# Reverse to get chronological order for the LLM  
           for doc in reversed(chat\_history\_docs):  
               message\_data \= doc.to\_dict()  
               formatted\_history.append(f"{message\_data\['role'\].capitalize()}: {message\_data\['text'\]}")  
           history\_string \= "\\n".join(formatted\_history) if formatted\_history else "No previous conversation."  
           logging.info(f"Chat history included: {history\_string}")

           \# \--- 2\. Retrieve Document Context (RAG) \---  
           \# a. Get embedding for the user's current message  
           user\_embedding\_response \= embedding\_model.predict(\[user\_message\])  
           user\_embedding \= np.array(user\_embedding\_response.embeddings\[0\].values).reshape(1, \-1) \# Reshape for cosine\_similarity

           relevant\_document\_chunks \= \[\]  
           \# b. Fetch all chunks from processed documents for this user  
           processed\_docs\_query \= db.collection(f'artifacts/{PROJECT\_ID}/users/{user\_id}/documents').where('status', '==', 'Processed')  
           processed\_docs\_snapshot \= processed\_docs\_query.get()

           all\_chunks\_data \= \[\]  
           for doc\_snap in processed\_docs\_snapshot:  
               doc\_chunks\_ref \= db.collection(f'artifacts/{PROJECT\_ID}/users/{user\_id}/documents').document(doc\_snap.id).collection('chunks')  
               chunks\_snapshot \= doc\_chunks\_ref.get()  
               for chunk\_doc in chunks\_snapshot:  
                   chunk\_data \= chunk\_doc.to\_dict()  
                   if 'embedding' in chunk\_data and 'text' in chunk\_data:  
                       all\_chunks\_data.append({  
                           'text': chunk\_data\['text'\],  
                           'embedding': np.array(chunk\_data\['embedding'\]).reshape(1, \-1)  
                       })

           \# c. Calculate similarity and select top K chunks  
           if all\_chunks\_data:  
               \# Extract embeddings and texts for similarity calculation  
               chunk\_embeddings \= np.array(\[data\['embedding'\]\[0\] for data in all\_chunks\_data\])  
               chunk\_texts \= \[data\['text'\] for data in all\_chunks\_data\]

               \# Calculate cosine similarity  
               similarities \= cosine\_similarity(user\_embedding, chunk\_embeddings)\[0\]

               \# Get top K (e.g., top 5\) relevant chunks  
               top\_k\_indices \= similarities.argsort()\[-5:\]\[::-1\] \# Get indices of top 5  
               relevant\_document\_chunks \= \[chunk\_texts\[i\] for i in top\_k\_indices if similarities\[i\] \> 0.7\] \# Only include if similarity is high

           document\_context\_string \= "\\n\\n---\\n\\n".join(relevant\_document\_chunks) if relevant\_document\_chunks else "No highly relevant document context found."  
           logging.info(f"Document context retrieved: {document\_context\_string}")

           \# \--- 3\. Construct the Full Prompt for Gemini \---  
           system\_prompt \= """  
               You are an expert Product Manager AI assistant designed to help users build Product Requirements Documents (PRDs).  
               Your primary goal is to answer questions and generate content strictly based on the provided document context AND the ongoing conversation history.  
               Adhere to the following guidelines:  
               \- If a user asks a question, identify the relevant information from the provided document context to formulate a clear and concise answer.  
               \- When generating PRD sections or content, use the information from the documents as the source of truth.  
               \- Maintain a professional, clear, and action-oriented tone, typical of a well-written PRD.  
               \- Avoid making up information. If the answer or required information is not present in the provided document context or conversation history, explicitly state:  
                 "I cannot find that specific information in the provided documents or previous conversation. Please ensure the relevant details are in an uploaded document, provide them directly, or ask a different question."  
               \- Encourage the user to upload more documents or clarify their request if the context is insufficient.  
               \- For PRD sections, provide structured, bullet-point, or numbered lists where appropriate for clarity.  
               \- Focus on the "what" and "why" from the documents, helping to shape requirements and goals.  
               \- IMPORTANT: Take into account the previous turns of the conversation to maintain context and continuity.  
           """

           \# Combine parts into a multi-turn chat format for Gemini  
           full\_prompt\_parts \= \[  
               {"role": "user", "parts": \[{"text": system\_prompt}\]},  
               {"role": "user", "parts": \[{"text": f"--- Conversation History \---\\n{history\_string}"}\]},  
               {"role": "user", "parts": \[{"text": f"--- Document Context \---\\n{document\_context\_string}"}\]},  
               {"role": "user", "parts": \[{"text": f"--- Current User Question \---\\n{user\_message}"}\]}  
           \]

           \# \--- 4\. Call Gemini API \---  
           response \= text\_model.generate\_content(  
               full\_prompt\_parts,  
               generation\_config={  
                   "max\_output\_tokens": 2048, \# Increased output tokens for potentially longer PRD sections  
                   "temperature": 0.7,  
                   "top\_p": 1,  
                   "top\_k": 40  
               }  
           )

           ai\_response \= response.text  
           logging.info(f"AI response: {ai\_response}")

           return jsonify({"response": ai\_response}), 200, headers

       except Exception as e:  
           logging.error(f"Error in chatWithDocument: {e}", exc\_info=True)  
           return jsonify({"error": str(e)}), 500, headers

### **Step 4.5: Implement exportPRD Cloud Function (Generates PRD, Not Raw History)**

This function will generate structured PRD content (possibly by calling the AI again with specific PRD generation instructions) and provide it as a Word document.

1. **Add exportPRD to functions/main.py:**  
   \# ... (Existing imports and initialization)

   @https\_fn.on\_request(region=REGION)  
   def exportPRD(req: https\_fn.Request):  
       """  
       Cloud Function that generates a comprehensive PRD based on all processed documents  
       and chat history, formats it, and returns a temporary download URL for a Word document.  
       """  
       logging.info("Export PRD request received.")  
       \# Handle CORS preflight request  
       if req.method \== 'OPTIONS':  
           headers \= {  
               'Access-Control-Allow-Origin': '\*',  
               'Access-Control-Allow-Methods': 'POST, OPTIONS',  
               'Access-Control-Allow-Headers': 'Content-Type, Authorization',  
               'Access-Control-Max-Age': '3600'  
           }  
           return https\_fn.Response('', headers=headers, status=204)

       headers \= {  
           'Access-Control-Allow-Origin': '\*',  
           'Content-Type': 'application/json'  
       }

       try:  
           request\_json \= req.get\_json(silent=True)  
           if not request\_json:  
               return jsonify({"error": "Invalid JSON"}), 400, headers

           user\_id \= request\_json.get('userId')  
           \# prd\_instructions \= request\_json.get('prdInstructions', "Generate a comprehensive Product Requirements Document (PRD)")

           if not user\_id:  
               return jsonify({"error": "Missing userId"}), 400, headers

           logging.info(f"User {user\_id} requesting PRD export.")

           \# \--- 1\. Gather all processed document content \---  
           all\_document\_text \= \[\]  
           docs\_snap \= db.collection(f'artifacts/{PROJECT\_ID}/users/{user\_id}/documents').where('status', '==', 'Processed').get()  
           for doc\_snap in docs\_snap:  
               doc\_data \= doc\_snap.to\_dict()  
               \# Retrieve all chunks for this document and concatenate  
               chunks\_ref \= db.collection(f'artifacts/{PROJECT\_ID}/users/{user\_id}/documents').document(doc\_snap.id).collection('chunks')  
               chunks\_snap \= chunks\_ref.order\_by('chunk\_index').get() \# Order by index to maintain original order  
               doc\_full\_text \= "".join(\[c.to\_dict()\['text'\] for c in chunks\_snap if 'text' in c.to\_dict()\])  
               if doc\_full\_text:  
                   all\_document\_text.append(f"Document: {doc\_data.get('name', 'Unnamed Document')}\\n{doc\_full\_text}")

           combined\_doc\_context \= "\\n\\n---\\n\\n".join(all\_document\_text)  
           if not combined\_doc\_context.strip():  
               return jsonify({"error": "No processed documents available to generate PRD."}), 404, headers

           \# \--- 2\. Gather relevant chat history for additional context \---  
           chat\_history\_query \= db.collection(f'artifacts/{PROJECT\_ID}/users/{user\_id}/chatHistory').order\_by('timestamp', direction=firestore.Query.DESCENDING).limit(20) \# More history for PRD  
           chat\_history\_docs \= chat\_history\_query.get()  
           formatted\_chat\_history \= \[\]  
           for doc in reversed(chat\_history\_docs):  
               message\_data \= doc.to\_dict()  
               formatted\_chat\_history.append(f"{message\_data\['role'\].capitalize()}: {message\_data\['text'\]}")  
           history\_string \= "\\n".join(formatted\_chat\_history) if formatted\_chat\_history else "No previous conversation."

           \# \--- 3\. Call Gemini to generate structured PRD content \---  
           \# This is a key difference: asking AI to GENERATE a PRD, not just summarize chat.  
           prd\_generation\_prompt \= f"""  
           Based on the following document content and the preceding conversation, generate a comprehensive Product Requirements Document (PRD).  
           Structure the PRD with clear headings and bullet points. Include sections like:  
           1\.  \*\*Introduction/Overview\*\*: What is the product/feature?  
           2\.  \*\*Goals & Objectives\*\*: What problem are we solving? What are the key metrics?  
           3\.  \*\*User Stories/Personas\*\*: Who are the users and what are their needs?  
           4\.  \*\*Features & Functionality\*\*: Detailed description of what the product/feature will do.  
           5\.  \*\*Technical Requirements (High-level)\*\*: Any relevant technical constraints or considerations.  
           6\.  \*\*Out of Scope\*\*: What will NOT be part of this PRD.

           Focus on extracting and synthesizing information from the provided documents and the chat history.  
           If information for a section is not available, state that explicitly.

           \--- Document Content \---  
           {combined\_doc\_context}

           \--- Chat History \---  
           {history\_string}

           \--- PRD Draft \---  
           """

           \# Use a more capable model like gemini-1.5-pro for complex generation  
           prd\_model \= aiplatform.GenerativeModel(model\_name="gemini-1.5-pro")  
           logging.info("Calling Gemini 1.5 Pro for PRD generation...")  
           prd\_response \= prd\_model.generate\_content(  
               prd\_generation\_prompt,  
               generation\_config={  
                   "max\_output\_tokens": 4096, \# High output for a full PRD  
                   "temperature": 0.5, \# Lower temperature for more factual/less creative  
                   "top\_p": 0.9,  
                   "top\_k": 20  
               }  
           )  
           generated\_prd\_text \= prd\_response.text  
           logging.info("Gemini PRD generation complete.")

           \# \--- 4\. Generate Word Document from the generated PRD text \---  
           document \= Document()  
           document.add\_heading('Product Requirements Document', level=0) \# Main Title  
           document.add\_paragraph(f"Generated by Explo Chat-PRD | Date: {firestore.SERVER\_TIMESTAMP.SERVER\_TIMESTAMP().strftime('%Y-%m-%d %H:%M')}")  
           document.add\_paragraph(f"For User ID: {user\_id}")  
           document.add\_page\_break()

           \# Add the generated PRD content  
           \# Basic formatting: split by lines and add as paragraphs, bold for headings (heuristic)  
           for line in generated\_prd\_text.split('\\n'):  
               if line.strip().startswith('\*\*') and line.strip().endswith('\*\*'):  
                   document.add\_heading(line.strip().replace('\*\*',''), level=2)  
               elif line.strip().startswith('\#'): \# Handle markdown headings  
                   level \= line.count('\#')  
                   document.add\_heading(line.lstrip('\# ').strip(), level=min(level, 4))  
               else:  
                   document.add\_paragraph(line.strip())

           temp\_docx\_filename \= f"Explo\_PRD\_{user\_id}\_{os.urandom(8).hex()}.docx"  
           temp\_docx\_path \= os.path.join(tempfile.gettempdir(), temp\_docx\_filename)  
           document.save(temp\_docx\_path)  
           logging.info(f"Word document saved temporarily to {temp\_docx\_path}")

           \# \--- 5\. Upload to Cloud Storage \---  
           destination\_blob\_name \= f'artifacts/{PROJECT\_ID}/users/{user\_id}/exports/{temp\_docx\_filename}'  
           bucket\_name \= f'{PROJECT\_ID}.appspot.com'  
           bucket \= gcs.get\_bucket(bucket\_name)  
           blob \= bucket.blob(destination\_blob\_name)  
           blob.upload\_from\_filename(temp\_docx\_path)  
           logging.info(f"Generated PRD uploaded to gs://{bucket\_name}/{destination\_blob\_name}")

           \# \--- 6\. Generate Signed URL for download \---  
           download\_url \= blob.generate\_signed\_url(expiration=3600, version='v4') \# Expires in 1 hour  
           logging.info(f"Generated download URL: {download\_url}")

           return jsonify({"downloadURL": download\_url}), 200, headers

       except Exception as e:  
           logging.error(f"Error in exportPRD: {e}", exc\_info=True)  
           return jsonify({"error": str(e)}), 500, headers  
       finally:  
           if 'temp\_docx\_path' in locals() and os.path.exists(temp\_docx\_path):  
               os.remove(temp\_docx\_path)  
               logging.info(f"Cleaned up temporary file: {temp\_docx\_path}")

### **Step 4.6: Enable APIs & Configure Cloud Functions**

1. **Enable APIs:** In your [Google Cloud Console](https://console.cloud.google.com/) (which your Firebase project is linked to), go to "APIs & Services" \-\> "Enabled APIs & Services". Ensure these are enabled:  
   * Cloud Functions API  
   * Cloud Storage API  
   * Cloud Firestore API  
   * Vertex AI API  
   * (Optional: Cloud Document AI API if you use it for advanced parsing)  
2. **Upgrade to Blaze Plan:** In your [Firebase Console](https://console.firebase.google.com/), under "Usage and Billing," ensure your project is on the **Blaze (pay-as-you-go)** plan. Cloud Functions and external API calls (like Gemini) require this. You won't be charged unless you exceed the free tier.  
3. **Set Environment Variables (IMPORTANT):**  
   * Your Cloud Functions need your Google Cloud Project ID and Region to initialize Vertex AI correctly. Add them to firebase.json for functions deployment:

{  
  "functions": {  
    "runtime": "python311", // or python312 depending on your choice  
    "source": "functions",  
    "env": {  
      "GCP\_PROJECT": "YOUR\_PROJECT\_ID", // Replace with your actual Project ID  
      "FUNCTION\_REGION": "us-central1" // Replace with your chosen region, e.g., us-central1, europe-west1  
    }  
  },  
  "hosting": {  
    "public": "public",  
    "ignore": \[  
      "firebase.json",  
      "\*\*/.\*",  
      "\*\*/node\_modules/\*\*"  
    \],  
    "rewrites": \[  
      {  
        "source": "\*\*",  
        "destination": "/index.html"  
      }  
    \]  
  },  
  "firestore": {  
    "rules": "firestore.rules",  
    "indexes": "firestore.indexes.json"  
  },  
  "storage": {  
    "rules": "storage.rules"  
  }  
}

## **Phase 5: Deployment & Initial Testing**

Now, you'll put all the pieces together and make your app live.

### **Step 5.1: Deploy Your Application**

1. **Open Terminal:** Navigate to your project's **root directory** (my-chat-prd-app).  
2. **Deploy Command:** Run the following command to deploy your entire application (frontend, functions, and rules):  
   firebase deploy

   * This command will:  
     * Deploy your public/ folder to Firebase Hosting.  
     * Build and deploy your Python Cloud Functions from functions/.  
     * Apply your firestore.rules and storage.rules.  
   * The deployment process might take several minutes, especially for Cloud Functions.

### **Step 5.2: Get Your Live URL & Test**

1. **Deployment Output:** After successful deployment, the CLI will provide your "Hosting URL":  
   ✔  Deploy complete\!

   Project Console: https://console.firebase.google.com/project/YOUR\_PROJECT\_ID/overview  
   Hosting URL: https://YOUR\_PROJECT\_ID.web.app

2. **Open in Browser:** Copy the Hosting URL and paste it into your web browser.  
3. **Thorough Testing:**  
   * **Authentication:** Verify the User ID is displayed.  
   * **Document Upload:** Upload PDF and Word files. Check the uploadStatus and uploadedDocumentsList for updates. Observe the spinner.  
   * **Delete Document:** Test the delete button for uploaded documents.  
   * **Chat Interaction:**  
     * Send simple messages.  
     * Ask questions related to your uploaded documents.  
     * Test multi-turn conversations to see if the AI remembers context.  
     * Observe the chatSpinner and chatStatus.  
     * Ask questions where the answer is *not* in the document to test the "I cannot find that information" response.  
     * Check for basic Markdown formatting in AI responses (bold, italics, lists).  
   * **Export PRD:** After some chat and document uploads, try exporting the PRD. Observe the exportSpinner and uploadStatus. Verify the downloaded .docx file contains a structured PRD generated by the AI, not just raw chat history.  
   * **Error Handling:** Observe status messages for any errors. Check your Firebase Functions logs in the Firebase Console if things aren't working as expected.

## **Key Advanced Components Integrated:**

* **Robust Document Parsing:** The processDocument function uses pypdf and python-docx. For more complex scanned documents or highly structured data, consider integrating **Google Cloud Document AI** within this function for advanced OCR and entity extraction.  
* **Advanced RAG with Firestore as Vector Store (Simple):**  
  * processDocument now chunks text and stores embeddings in a Firestore subcollection (documents/{docId}/chunks).  
  * chatWithDocument calculates the similarity between the user's query embedding and these stored chunk embeddings, retrieving the most relevant ones.  
  * **WARNING:** While this demonstrates RAG, for very large document sets or high query volumes, a **dedicated vector database** (e.g., Pinecone, Weaviate, ChromaDB, or Google's native Vector Search) is highly recommended for scalability and performance. This would require replacing the Firestore chunk storage and retrieval logic with calls to your chosen vector DB's API.  
* **Long-Term Conversation Memory:** chatWithDocument now explicitly fetches and includes the last 10 chat messages (both user and AI) in the prompt, allowing for conversational continuity.  
* **Streamlined PRD Generation (Export):** The exportPRD function now actively prompts a more capable Gemini model (gemini-1.5-pro) to *generate* a structured PRD based on all uploaded document content and chat history, rather than simply exporting raw chat logs.  
* **Improved Frontend Feedback:** Loading spinners are added to chat and export buttons, and showStatus is enhanced for clearer messages.  
* **Delete Document Feature:** Users can now delete uploaded documents, which removes them from both Cloud Storage and Firestore.

This comprehensive plan provides a powerful starting point for your Chat-PRD page. Building this involves significant work on both the frontend and backend, especially around the AI logic. Good luck\!