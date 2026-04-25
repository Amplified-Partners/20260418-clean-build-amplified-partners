export default function WritingPanel() {
  const drafts = [
    { title: 'Pudding Logic: F1 meets Accounting', status: 'Drafting' },
    { title: 'Sovereign Engine announcement', status: 'Outline' },
    { title: 'Graffiti database intro post', status: 'Idea' },
  ];

  return (
    <div className="glass-card" id="writing-panel">
      <div className="card-label">Writing</div>
      <ul className="writing-list">
        {drafts.map((d, i) => (
          <li key={i} className="writing-item">
            <span className="writing-item__title">{d.title}</span>
            <span className={`writing-badge writing-badge--${d.status.toLowerCase()}`}>
              {d.status}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
