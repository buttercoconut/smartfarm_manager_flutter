"""Dashboard screen showing sensor data list."""

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../services/api_service.dart';

final apiProvider = Provider((ref) => ApiService(baseUrl: 'http://localhost:8000'));

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final api = ref.watch(apiProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('SmartFarm Dashboard')),
      body: FutureBuilder<List>(
        future: api.fetchSensorData(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          final data = snapshot.data ?? [];
          return ListView.builder(
            itemCount: data.length,
            itemBuilder: (context, index) {
              final item = data[index];
              return ListTile(
                title: Text('Sensor ${item['sensor_id']}'),
                subtitle: Text('Temp: ${item['temperature']}°C, Humidity: ${item['humidity']}%'),
              );
            },
          );
        },
      ),
    );
  }
}
