import 'package:flutter/material.dart';

void main() => runApp(const WorkBoardApp());

class WorkBoardApp extends StatelessWidget {
  const WorkBoardApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'WorkBoard',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.indigo),
      home: const TaskListScreen(),
    );
  }
}

class TaskListScreen extends StatefulWidget {
  const TaskListScreen({super.key});

  @override
  State<TaskListScreen> createState() => _TaskListScreenState();
}

class _TaskListScreenState extends State<TaskListScreen> {
  // Starter chỉ giữ title trong bộ nhớ. Tuần 04–07 thay bằng WorkTask.
  final List<String> _titles = [];

  Future<void> _addTask() async {
    final title = await showDialog<String>(
      context: context,
      builder: (context) => const AddTaskDialog(),
    );
    if (!mounted || title == null) return;
    setState(() => _titles.add(title));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('WorkBoard')),
      body: SafeArea(
        child: _titles.isEmpty
            ? const Center(
                child: Padding(
                  padding: EdgeInsets.all(24),
                  child: Text(
                    'Chưa có công việc\nThêm công việc đầu tiên để bắt đầu.',
                    textAlign: TextAlign.center,
                  ),
                ),
              )
            : ListView.separated(
                padding: const EdgeInsets.only(bottom: 96),
                itemCount: _titles.length,
                separatorBuilder: (context, index) => const Divider(height: 1),
                itemBuilder: (context, index) => ListTile(
                  title: Text(_titles[index]),
                  subtitle: const Text('Chưa hoàn thành'),
                ),
              ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _addTask,
        tooltip: 'Thêm công việc',
        child: const Icon(Icons.add),
      ),
    );
  }
}

class AddTaskDialog extends StatefulWidget {
  const AddTaskDialog({super.key});

  @override
  State<AddTaskDialog> createState() => _AddTaskDialogState();
}

class _AddTaskDialogState extends State<AddTaskDialog> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();

  @override
  void dispose() {
    _titleController.dispose();
    super.dispose();
  }

  void _submit() {
    if (!_formKey.currentState!.validate()) return;
    Navigator.of(context).pop(_titleController.text.trim());
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Công việc mới'),
      content: SingleChildScrollView(
        child: Form(
          key: _formKey,
          child: TextFormField(
            key: const ValueKey('task-title'),
            controller: _titleController,
            autofocus: true,
            decoration: const InputDecoration(labelText: 'Tiêu đề'),
            textInputAction: TextInputAction.done,
            onFieldSubmitted: (_) => _submit(),
            validator: (value) {
              final title = (value ?? '').trim();
              if (title.isEmpty) return 'Nhập tiêu đề công việc';
              if (title.length > 120) return 'Tiêu đề tối đa 120 ký tự';
              return null;
            },
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Hủy'),
        ),
        FilledButton(onPressed: _submit, child: const Text('Lưu')),
      ],
    );
  }
}
