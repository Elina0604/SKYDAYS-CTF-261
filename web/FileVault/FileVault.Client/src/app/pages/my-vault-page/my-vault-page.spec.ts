import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MyVaultPage } from './my-vault-page';

describe('MyVaultPage', () => {
  let component: MyVaultPage;
  let fixture: ComponentFixture<MyVaultPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MyVaultPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MyVaultPage);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
