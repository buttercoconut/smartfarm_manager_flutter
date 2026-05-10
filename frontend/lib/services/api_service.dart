import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/plant.dart';
import '../models/sensor.dart';
import '../models/environment.dart';

class ApiService {
  final String _baseUrl = 'https://api.smartfarm.example.com';

  Future<List<Plant>> fetchPlants() async {
    final response = await http.get(Uri.parse('$_baseUrl/plants'));
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body) as List<dynamic>;
      return data.map((e) => Plant.fromJson(e as Map<String, dynamic>)).toList();
    } else {
      throw Exception('Failed to load plants');
    }
  }

  Future<List<Sensor>> fetchSensors(String plantId) async {
    final response = await http.get(Uri.parse('$_baseUrl/plants/$plantId/sensors'));
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body) as List<dynamic>;
      return data.map((e) => Sensor.fromJson(e as Map<String, dynamic>)).toList();
    } else {
      throw Exception('Failed to load sensors');
    }
  }

  Future<Environment> fetchEnvironment(String plantId) async {
    final response = await http.get(Uri.parse('$_baseUrl/plants/$plantId/environment'));
    if (response.statusCode == 200) {
      final Map<String, dynamic> data = jsonDecode(response.body) as Map<String, dynamic>;
      return Environment.fromJson(data);
    } else {
      throw Exception('Failed to load environment');
    }
  }
}
