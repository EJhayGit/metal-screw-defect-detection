import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:image_picker/image_picker.dart';

class ApiService {
  // 10.0.2.2 is used for Android emulator to access the host machine's localhost.
  // 127.0.0.1 is used for iOS simulator or desktop apps.
  // localhost is strictly used for Web to avoid browser CORS/Private Network blocks.
  static String get baseUrl {
    if (kIsWeb) {
      return 'http://localhost:8000';
    } else if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000';
    } else {
      return 'http://127.0.0.1:8000';
    }
  }

  /// Quick health check to verify the backend is reachable before uploading.
  static Future<bool> isBackendReachable() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/health'),
      ).timeout(
        const Duration(seconds: 5),
        onTimeout: () => http.Response('', 408),
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  static Future<Map<String, dynamic>> classifyImage(XFile imageFile) async {
    // Step 1: Check backend connectivity first (fast fail)
    final reachable = await isBackendReachable();
    if (!reachable) {
      throw Exception(
        'Cannot connect to the backend server.\n\n'
        'Please ensure:\n'
        '1. The backend is running (python main.py)\n'
        '2. It is listening on port 8000\n'
        '3. Your device and computer are on the same network',
      );
    }

    // Step 2: Upload and classify with retry
    const maxRetries = 2;
    Exception? lastError;

    for (int attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        var request = http.MultipartRequest(
          'POST',
          Uri.parse('$baseUrl/predict'),
        );

        final bytes = await imageFile.readAsBytes();
        request.files.add(
          http.MultipartFile.fromBytes(
            'file',
            bytes,
            filename: imageFile.name,
          ),
        );

        var streamedResponse = await request.send().timeout(
          const Duration(seconds: 30),
          onTimeout: () {
            throw Exception(
              'Request timed out. The server may be busy processing. '
              'Please try again.',
            );
          },
        );
        var response = await http.Response.fromStream(streamedResponse);

        if (response.statusCode == 200) {
          return json.decode(response.body);
        } else {
          throw Exception(
            'Server returned error ${response.statusCode}: ${response.body}',
          );
        }
      } catch (e) {
        lastError = e is Exception ? e : Exception(e.toString());
        if (attempt < maxRetries) {
          // Wait briefly before retrying
          await Future.delayed(Duration(seconds: 1 * (attempt + 1)));
          continue;
        }
      }
    }

    throw lastError ?? Exception('Failed to classify image after retries.');
  }
}
