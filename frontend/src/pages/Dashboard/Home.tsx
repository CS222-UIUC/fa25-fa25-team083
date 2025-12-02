import PageMeta from "../../components/common/PageMeta";
import RemoteData from "../../components/dashboard/RemoteData";

export default function Home() {
  return (
    <>
      <PageMeta
        title="Space Hub Dashboard"
        description="Live NASA & external endpoints dashboard"
      />

      <div className="grid grid-cols-12 gap-4 md:gap-6">
        <div className="col-span-12 space-y-6">
          <RemoteData />
        </div>
      </div>
    </>
  );
}
