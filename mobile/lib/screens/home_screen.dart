import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:image_picker/image_picker.dart';
import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  XFile? _image;
  final ImagePicker _picker = ImagePicker();
  bool _isLoading = false;
  String? _classificationResult;
  double? _confidence;

  Future<void> _pickImage(ImageSource source) async {
    try {
      final pickedFile = await _picker.pickImage(source: source);
      if (pickedFile != null) {
        setState(() {
          _image = pickedFile;
          _classificationResult = null; // reset previous result
          _confidence = null;
        });
        _uploadAndClassify();
      }
    } catch (e) {
      _showError('Error picking image: $e');
    }
  }

  Future<void> _uploadAndClassify() async {
    if (_image == null) return;

    setState(() {
      _isLoading = true;
    });

    try {
      final result = await ApiService.classifyImage(_image!);
      setState(() {
        _classificationResult = result['classification'];
        _confidence = result['confidence'];
      });
    } catch (e) {
      _showError(e.toString());
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _showError(String message) {
    // Clean up the exception wrapper text for display
    String cleanMessage = message.replaceAll('Exception: ', '').replaceAll('Exception:', '');
    
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Row(
          children: [
            Icon(Icons.error_outline, color: Colors.red),
            SizedBox(width: 8),
            Text('Connection Error'),
          ],
        ),
        content: Text(cleanMessage),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text('OK'),
          ),
          if (_image != null)
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                _uploadAndClassify();
              },
              child: Text('Retry'),
            ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Metal Screw Defect Detector')),
      body: SingleChildScrollView(
        child: Column(
          children: [
            SizedBox(height: 20),
            if (_image != null)
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(12.0),
                  child: kIsWeb
                      ? Image.network(_image!.path, height: 350, fit: BoxFit.cover)
                      : Image.file(File(_image!.path), height: 350, fit: BoxFit.cover),
                ),
              )
            else
              Container(
                height: 350,
                width: double.infinity,
                margin: const EdgeInsets.symmetric(horizontal: 16.0),
                decoration: BoxDecoration(
                  color: Colors.grey[200],
                  borderRadius: BorderRadius.circular(12.0),
                  border: Border.all(color: Colors.grey[400]!),
                ),
                child: Center(
                  child: Text(
                    'Please select or capture an image',
                    style: TextStyle(color: Colors.grey[600]),
                  ),
                ),
              ),
            SizedBox(height: 30),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton.icon(
                  icon: Icon(Icons.camera_alt),
                  label: Text('Camera'),
                  onPressed: () => _pickImage(ImageSource.camera),
                ),
                ElevatedButton.icon(
                  icon: Icon(Icons.photo_library),
                  label: Text('Gallery'),
                  onPressed: () => _pickImage(ImageSource.gallery),
                ),
              ],
            ),
            SizedBox(height: 40),
            if (_isLoading)
              CircularProgressIndicator()
            else if (_classificationResult != null)
              _buildResultsDashboard(),
          ],
        ),
      ),
    );
  }

  Widget _buildResultsDashboard() {
    bool isDefective = _classificationResult?.toLowerCase() == 'defective';
    Color resultColor = isDefective ? Colors.red : Colors.green;

    return Container(
      padding: const EdgeInsets.all(24.0),
      margin: const EdgeInsets.symmetric(horizontal: 16.0),
      width: double.infinity,
      decoration: BoxDecoration(
        color: resultColor.withOpacity(0.1),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: resultColor, width: 2),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                isDefective ? Icons.warning_amber_rounded : Icons.check_circle_outline,
                color: resultColor,
                size: 32,
              ),
              SizedBox(width: 12),
              Text(
                isDefective ? 'DEFECTIVE' : 'NORMAL',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: resultColor,
                ),
              ),
            ],
          ),
          SizedBox(height: 12),
          if (_confidence != null)
            Text(
              'Confidence Score: ${(_confidence! * 100).toStringAsFixed(1)}%',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w500,
                color: Colors.black87,
              ),
            ),
        ],
      ),
    );
  }
}
