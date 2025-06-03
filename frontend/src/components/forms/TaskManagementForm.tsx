import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "../ui/Button";
import { Input } from "../ui/Input";
import { Card } from "../ui/Card";
import { useUpdateTask } from "../../hooks/api";
import { TaskStatus, TaskPriority, Task } from "../../types";

const taskUpdateSchema = z.object({
  status: z.enum([
    "pending",
    "assigned",
    "in_progress",
    "completed",
    "cancelled",
  ]),
  priority: z.enum(["low", "medium", "high", "critical"]),
  assignedTo: z.string().optional(),
  notes: z.string().optional(),
  estimatedTime: z.number().min(0).optional(),
});

type TaskUpdateForm = z.infer<typeof taskUpdateSchema>;

interface TaskManagementFormProps {
  task: Task;
  onClose: () => void;
}

export const TaskManagementForm: React.FC<TaskManagementFormProps> = ({
  task,
  onClose,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<TaskUpdateForm>({
    resolver: zodResolver(taskUpdateSchema),
    defaultValues: {
      status: task.status,
      priority: task.priority,
      assignedTo: task.assignedTo || "",
      notes: task.notes || "",
      estimatedTime: task.estimatedTime || 0,
    },
  });

  const updateTaskMutation = useUpdateTask();

  const onSubmit = async (data: TaskUpdateForm) => {
    try {
      await updateTaskMutation.mutateAsync({
        id: task.id,
        updates: data,
      });
      onClose();
    } catch (error) {
      console.error("Failed to update task:", error);
    }
  };

  const statusOptions: { value: TaskStatus; label: string }[] = [
    { value: "pending", label: "Pending" },
    { value: "assigned", label: "Assigned" },
    { value: "in_progress", label: "In Progress" },
    { value: "completed", label: "Completed" },
    { value: "cancelled", label: "Cancelled" },
  ];

  const priorityOptions: { value: TaskPriority; label: string }[] = [
    { value: "low", label: "Low" },
    { value: "medium", label: "Medium" },
    { value: "high", label: "High" },
    { value: "critical", label: "Critical" },
  ];

  return (
    <Card className="max-w-2xl mx-auto p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Update Task</h2>
        <p className="text-gray-600">{task.title}</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Status
            </label>
            <select
              {...register("status")}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {statusOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            {errors.status && (
              <p className="mt-1 text-sm text-red-600">
                {errors.status.message}
              </p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Priority
            </label>
            <select
              {...register("priority")}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {priorityOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            {errors.priority && (
              <p className="mt-1 text-sm text-red-600">
                {errors.priority.message}
              </p>
            )}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Assigned To (User ID)
          </label>
          <Input
            {...register("assignedTo")}
            placeholder="Enter user ID to assign task"
            error={errors.assignedTo?.message}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Estimated Time (hours)
          </label>
          <Input
            type="number"
            step="0.5"
            min="0"
            {...register("estimatedTime", { valueAsNumber: true })}
            placeholder="0"
            error={errors.estimatedTime?.message}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Notes
          </label>
          <textarea
            {...register("notes")}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Add any notes or updates..."
          />
          {errors.notes && (
            <p className="mt-1 text-sm text-red-600">{errors.notes.message}</p>
          )}
        </div>

        <div className="flex justify-end space-x-4">
          <Button
            type="button"
            variant="outline"
            onClick={onClose}
            disabled={isSubmitting}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={isSubmitting} loading={isSubmitting}>
            Update Task
          </Button>
        </div>
      </form>
    </Card>
  );
};
