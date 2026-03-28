name: react-native-fastapi-upload
description: Use this skill whenever you need to send an image captured from the Expo Camera or chosen from the Expo Image Picker to the Python FastAPI backend for CNN classification.

## Execution Rules
1. **FormData Formatting:** Always use standard `FormData` to append the image payload. You must extract the `uri`, `type` (e.g., 'image/jpeg'), and a generic `name` from the Expo asset object.
2. **Network Request:** Use the native `fetch` API. Set the method to `POST`. Do not manually set the `Content-Type` header to `multipart/form-data`; let the `fetch` API automatically set it with the correct boundary.
3. **Endpoint:** Direct the payload to the `/predict` or `/classify` route on the FastAPI server.
4. **State Management:** Ensure a loading state (e.g., `<ActivityIndicator>`) is toggled true before the fetch begins and false in the `finally` block.
5. **Error Handling:** Wrap the network call in a `try/catch` block and display a user-friendly alert if the Python server is unreachable or if the model fails to process the image.