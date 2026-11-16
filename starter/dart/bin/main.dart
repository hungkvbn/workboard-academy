import 'dart:convert';

import 'package:workboard_dart/workboard_dart.dart';

void main() {
  final task = WorkTask(
    id: 'demo-001',
    title: '  Đọc bài Dart đầu tiên  ',
    updatedAt: DateTime.utc(2026, 1, 1, 9),
    ownerId: 'learner-1',
  );
  final completed = task.copyWith(status: TaskStatus.done);
  print('Bản gốc: ${task.title} — ${task.status.name}');
  print('Bản sao: ${completed.title} — ${completed.status.name}');
  print(const JsonEncoder.withIndent('  ').convert(completed.toJson()));
}
