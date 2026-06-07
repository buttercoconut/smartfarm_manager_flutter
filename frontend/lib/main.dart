"""Flutter project entry point (minimal)."""

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'services/api_service.dart';
import 'screens/dashboard_screen.dart';

void main() {
  runApp(const ProviderScope(child: SmartFarmApp()));
}

class SmartFarmApp extends ConsumerWidget {
  const SmartFarmApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp(
      title: 'SmartFarm Manager',
      theme: ThemeData(primarySwatch: Colors.green),
      home: const DashboardScreen(),
    );
  }
