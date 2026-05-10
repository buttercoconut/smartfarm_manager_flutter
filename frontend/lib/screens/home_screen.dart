import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
import '../services/websocket_service.dart';
import '../widgets/environment_chart.dart';
import '../widgets/sensor_card.dart';
import '../models/environment.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    Provider.of<WebSocketService>(context, listen: false).connect();
  }

  @override
  Widget build(BuildContext context) {
    final ws = Provider.of<WebSocketService>(context);
    final env = ws.environment;
    final sensors = ws.sensors;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Smart Farm Dashboard'),
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          // Force a refresh if needed
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              if (env != null) EnvironmentChart(data: [env]),
              const SizedBox(height: 20),
              const Text(
                'Sensors',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              Wrap(
                spacing: 12,
                runSpacing: 12,
                children: sensors
                    .map((s) => SizedBox(
                          width: 160,
                          child: SensorCard(sensor: s),
                        ))
                    .toList(),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
