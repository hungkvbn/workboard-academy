import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:workboard_app/main.dart';

void main() {
  testWidgets('Bắt đầu bằng trạng thái rỗng', (tester) async {
    await tester.pumpWidget(const WorkBoardApp());
    expect(find.text('WorkBoard'), findsOneWidget);
    expect(find.textContaining('Chưa có công việc'), findsOneWidget);
  });

  testWidgets('Thêm một tiêu đề hợp lệ và trim khoảng trắng', (tester) async {
    await tester.pumpWidget(const WorkBoardApp());
    await tester.tap(find.byTooltip('Thêm công việc'));
    await tester.pumpAndSettle();
    await tester.enterText(find.byKey(const ValueKey('task-title')), '  Học Dart  ');
    await tester.tap(find.text('Lưu'));
    await tester.pumpAndSettle();
    expect(find.text('Học Dart'), findsOneWidget);
    expect(find.textContaining('Chưa có công việc'), findsNothing);
  });

  testWidgets('Tiêu đề trắng hiển thị validation và không đóng form', (tester) async {
    await tester.pumpWidget(const WorkBoardApp());
    await tester.tap(find.byTooltip('Thêm công việc'));
    await tester.pumpAndSettle();
    await tester.enterText(find.byKey(const ValueKey('task-title')), '   ');
    await tester.tap(find.text('Lưu'));
    await tester.pumpAndSettle();
    expect(find.text('Nhập tiêu đề công việc'), findsOneWidget);
    expect(find.byType(AddTaskDialog), findsOneWidget);
  });
}
