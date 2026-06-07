"""API client using http package."""

import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;

  ApiService({required this.baseUrl});

  Future<List<dynamic>> fetchSensorData() async {
    final response = await http.get(Uri.parse('$baseUrl/api/sensor/'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load sensor data');
    }
  }
}
