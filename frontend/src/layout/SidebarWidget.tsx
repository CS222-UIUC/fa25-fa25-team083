export default function SidebarWidget() {
  return (
    <div
      className={`
        mx-auto mb-10 w-full max-w-60 rounded-2xl bg-gray-50 px-4 py-5 text-center dark:bg-white/[0.03]`}
    >
      <h4 className="font-semibold text-gray-900 dark:text-white">Space Hub</h4>
      <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">&copy; {new Date().getFullYear()} - Space Hub</p>
    </div>
  );
}
