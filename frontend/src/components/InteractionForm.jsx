import { useSelector, useDispatch } from "react-redux";
import { updateField } from "../features/formSlice";
import { toast } from "react-toastify";

const InteractionForm = () => {
  const dispatch = useDispatch();
  const formData = useSelector((state) => state.form);

  const handleChange = (e) => {
    const { name, value } = e.target;
    dispatch(updateField({ field: name, value }));

    // Notify on manual change
    const label = name.replace("_", " ").toUpperCase();
    toast.success(`User Updated: ${label}`, {
      position: "top-right",
      autoClose: 10000,
      hideProgressBar: true,
      theme: "light",
    });
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm h-full overflow-y-auto border border-gray-200">
      <h2 className="text-xl font-bold mb-4 text-blue-900 border-b pb-2">
        Interaction Details
      </h2>

      <div className="space-y-5 text-sm">
        {/* HCP Name */}
        <div>
          <label className="block font-semibold text-gray-700">HCP Name</label>
          <select
            name="hcp_name"
            value={formData.hcp_name || ""}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-gray-50"
          >
            <option value="">Select HCP...</option>
            <option value="Dr. Smith">Dr. Smith</option>
            <option value="Dr. John">Dr. John</option>
            <option value="Dr. Emily">Dr. Emily</option>
            <option value="Dr. Sarah">Dr. Sarah</option>
          </select>
        </div>

        {/* Interaction Type & Date/Time Row */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block font-semibold text-gray-700">
              Interaction Type
            </label>
            <select
              name="interaction_type"
              value={formData.interaction_type || "Meeting"}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-gray-50"
            >
              <option value="Meeting">Meeting</option>
              <option value="Call">Call</option>
              <option value="Email">Email</option>
            </select>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block font-semibold text-gray-700">Date</label>
              <input
                type="date"
                name="date"
                value={formData.date || ""}
                onChange={handleChange}
                className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-gray-50"
              />
            </div>
            <div>
              <label className="block font-semibold text-gray-700">Time</label>
              <input
                type="time"
                name="time"
                value={formData.time || ""}
                onChange={handleChange}
                className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-gray-50"
              />
            </div>
          </div>
        </div>

        {/* Attendees - FIXED BINDING */}
        <div>
          <label className="block font-semibold text-gray-700">Attendees</label>
          <input
            type="text"
            name="attendees"
            value={
              Array.isArray(formData.attendees)
                ? formData.attendees.join(", ")
                : formData.attendees || ""
            }
            onChange={(e) => {
              const newValue = e.target.value.split(",").map((s) => s.trim());
              dispatch(updateField({ field: "attendees", value: newValue }));
              toast.success(`User Updated: ATTENDEES`, {
                autoClose: 10000,
                hideProgressBar: true,
              });
            }}
            placeholder="Enter names (e.g. Dr. Emily, Nurse Joy)"
            className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-gray-50"
          />
        </div>

        {/* Topics Discussed */}
        <div>
          <label className="block font-semibold text-gray-700">
            Topics Discussed
          </label>
          <textarea
            name="topics_discussed"
            value={formData.topics_discussed || ""}
            onChange={handleChange}
            rows="3"
            placeholder="Key discussion points..."
            className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-gray-50"
          ></textarea>
        </div>

        {/* Sentiment */}
        <div>
          <label className="block font-semibold text-gray-700 mb-2">
            HCP Sentiment
          </label>
          <div className="flex space-x-6 bg-gray-50 p-2 rounded-md border border-gray-200">
            {["Positive", "Neutral", "Negative"].map((s) => (
              <label key={s} className="flex items-center cursor-pointer">
                <input
                  type="radio"
                  name="sentiment"
                  value={s}
                  checked={formData.sentiment === s}
                  onChange={handleChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500"
                />
                <span className="ml-2 text-sm text-gray-700">{s}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Outcomes */}
        <div>
          <label className="block font-semibold text-gray-700">Outcomes</label>
          <textarea
            name="outcomes"
            value={formData.outcomes || ""}
            onChange={handleChange}
            rows="2"
            placeholder="What was the result?"
            className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-gray-50"
          ></textarea>
        </div>

        {/* Follow-up Actions */}
        <div>
          <label className="block font-semibold text-gray-700">
            Follow-up Actions
          </label>
          <textarea
            name="follow_up_actions"
            value={formData.follow_up_actions || ""}
            onChange={handleChange}
            rows="2"
            placeholder="Next steps..."
            className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-gray-50"
          ></textarea>
        </div>
      </div>
    </div>
  );
};

export default InteractionForm;
